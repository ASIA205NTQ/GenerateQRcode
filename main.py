import qrcode
from PIL import Image, ImageDraw, ImageFont
import csv
import os

# Hàm tạo QR code và chèn logo
def create_qr_with_logo(employee_code, employee_name, logo_path, output_path):
    # Tạo mã QR code từ link chứa mã số nhân viên
    qr_data = f"https://asia205ntq.github.io/CNXDSG/?employeeCode={employee_code}"  # Link mẫu có thể thay đổi theo yêu cầu

    qr = qrcode.QRCode(
        version=1,  # Kích thước của QR code
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Mức độ sửa lỗi để chèn logo (H cho phép lỗi cao)
        box_size=8,  # Kích thước của mỗi ô trong QR code
        border=4,  # Độ rộng của viền xung quanh QR code
    )
    
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Tạo hình ảnh QR code với màu nền trắng và màu tìm kiếm (finder patterns) màu xanh lá
    qr_img = qr.make_image(fill_color="green", back_color="white").convert('RGB')
    
    # Chèn logo ở giữa QR code
    logo = Image.open(logo_path)
    
    # Thay đổi kích thước logo (thu nhỏ chiều dọc một chút để logo gần vuông hơn)
    logo_width = qr_img.size[0] // 3  # Chiều rộng logo bằng 1/3 chiều rộng QR code
    logo_height = int(logo_width * 0.85)  # Chiều cao logo bằng 85% chiều rộng để gần vuông hơn
    logo_size = (logo_width, logo_height)
    logo = logo.resize(logo_size)
    
    # Tính toán vị trí để chèn logo vào giữa QR code
    logo_position = (
        (qr_img.size[0] - logo_size[0]) // 2,
        (qr_img.size[1] - logo_size[1]) // 2
    )
    
    # Chèn logo vào giữa QR code
    qr_img.paste(logo, logo_position, mask=logo)  # Sử dụng logo như một mặt nạ (mask)
    
    # Thêm không gian giữa QR code và viền đỏ
    padding = 50  # Tăng khoảng cách từ QR code đến khung viền đỏ
    
    # Tạo khung ảnh với viền đỏ và khoảng cách xa hơn
    width, height = qr_img.size
    img_with_padding = Image.new('RGB', (width + padding * 2, height + padding * 2), "white")  # Tạo không gian cho phần padding
    img_with_padding.paste(qr_img, (padding, padding))  # Dán QR code vào giữa hình ảnh với phần padding

    # Vẽ chữ Petrolimex Sài Gòn trong khoảng giữa QR code và viền đỏ
    draw = ImageDraw.Draw(img_with_padding)
    font_path = "C:/Windows/Fonts/arial.ttf"  # Đường dẫn đến font Arial
    font_petrolimex = ImageFont.truetype(font_path, 30)  # Kích thước chữ Petrolimex Sài Gòn
    petrolimex_text = "Petrolimex Sài Gòn"
    text_bbox = draw.textbbox((0, 0), petrolimex_text, font=font_petrolimex)
    text_width = text_bbox[2] - text_bbox[0]
    text_position = ((img_with_padding.size[0] - text_width) // 2, padding // 2)  # Căn giữa dòng chữ Petrolimex Sài Gòn
    
    draw.text(text_position, petrolimex_text, font=font_petrolimex, fill=(0, 0, 255))  # Màu xanh da trời và in đậm
    
    # Thêm dòng chữ "Quét QR để đánh giá" ở phía dưới QR code
    font_scan = ImageFont.truetype(font_path, 28)  # Kích thước chữ "Quét QR để đánh giá"
    scan_text = "Quét QR để đánh giá"
    scan_text_bbox = draw.textbbox((0, 0), scan_text, font=font_scan)
    scan_text_width = scan_text_bbox[2] - scan_text_bbox[0]
    scan_text_position = ((img_with_padding.size[0] - scan_text_width) // 2, height + padding + 10)  # Vị trí ở dưới QR code
    
    draw.text(scan_text_position, scan_text, font=font_scan, fill=(0, 0, 0))  # Màu đen
    
    # Thêm viền màu đỏ xung quanh QR code với khoảng cách xa hơn
    img_with_border = Image.new('RGB', (img_with_padding.size[0] + 20, img_with_padding.size[1] + 20), "red")  # Thêm viền màu đỏ xung quanh
    img_with_border.paste(img_with_padding, (10, 10))  # Dán QR code vào giữa hình ảnh với viền đỏ
    
    # Tạo hình ảnh kết hợp với thông tin mã số nhân viên và tên
    img_with_name = Image.new('RGB', (img_with_border.size[0], img_with_border.size[1] + 70), (255, 255, 255))  # Thêm không gian bên dưới để chứa thông tin
    img_with_name.paste(img_with_border, (0, 0))
    
    # Vẽ thông tin mã số nhân viên và tên nhân viên bên dưới QR code
    draw = ImageDraw.Draw(img_with_name)

    # Sử dụng font Arial hoặc một font hỗ trợ Unicode khác
    font = ImageFont.truetype(font_path, 32)  # Tăng kích thước font lên 32 và in đậm
    
    # Chuỗi hiển thị gồm mã số nhân viên và tên nhân viên với định dạng: "12345-Nguyễn Văn A"
    employee_info = f"{employee_code}-{employee_name}"
    
    # Lấy bounding box của văn bản để tính toán kích thước
    bbox = draw.textbbox((0, 0), employee_info, font=font)
    text_width = bbox[2] - bbox[0]  # Chiều rộng của văn bản
    text_height = bbox[3] - bbox[1]  # Chiều cao của văn bản
    text_position = ((img_with_name.size[0] - text_width) // 2, img_with_border.size[1] + (70 - text_height) // 2)  # Căn giữa theo cả chiều dọc và ngang
    
    draw.text(text_position, employee_info, font=font, fill=(0, 0, 0))  # Màu đen, in đậm
    
    # Thêm khung màu đen bao quanh toàn bộ hình ảnh
    final_img = Image.new('RGB', (img_with_name.size[0] + 10, img_with_name.size[1] + 10), "black")  # Tạo khung màu đen
    final_img.paste(img_with_name, (5, 5))  # Dán toàn bộ QR code vào giữa khung màu đen
    
    # Lưu hình ảnh QR code có logo, viền đỏ, thông tin nhân viên và khung đen
    final_img.save(output_path)

# Hàm đọc danh sách nhân viên từ file CSV và tạo mã QR code
def generate_qr_codes_from_csv(csv_file, logo_path, output_dir):
    # Tạo thư mục đầu ra nếu chưa tồn tại
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Mở file CSV với mã hóa UTF-8
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Bỏ qua dòng tiêu đề nếu có
        for row in reader:
            employee_code = row[0].strip()  # Mã số nhân viên, loại bỏ khoảng trắng không cần thiết
            employee_name = row[1].strip()  # Tên nhân viên, loại bỏ khoảng trắng không cần thiết
            output_path = f"{output_dir}/{employee_code}_{employee_name}.png"  # Tên file đầu ra
            
            create_qr_with_logo(employee_code, employee_name, logo_path, output_path)
            print(f"QR code cho {employee_name} ({employee_code}) đã được tạo.")

# Ví dụ gọi hàm
if __name__ == '__main__':
    csv_file = 'employee_list.csv'  # File CSV chứa mã nhân viên và tên
    logo_path = 'logo.png'  # Đường dẫn đến logo
    output_dir = 'qr_codes'  # Thư mục lưu QR code
    
    generate_qr_codes_from_csv(csv_file, logo_path, output_dir)
