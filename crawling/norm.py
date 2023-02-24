_CLASS = ['Ranger', 'Morning', 'Vios', 'Innova', 'Camry', 'C class', 'i10', 'Fortuner', 'SantaFe', 'E class', '3', 'GLC', 'Everest', 'Accent', 'CX5', 'Corolla altis', 'CRV', 'Lux A 2.0', 'S class', 'Cerato', 'Spark', 'RX', 'Tucson', 'City', 'Civic', 'Fadil', 'Xpander', 'Elantra', 'Lux SA 2.0', 'Corolla Cross', 'Yaris', 'Lacetti', 'Cruze', 'Transit', '6', 'Explorer', 'EcoSport', 'Prado', 'K3', 'Triton', 'Sorento', '5 Series', 'Range Rover', 'Outlander', 'Land Cruiser', 'BT50', 'Seltos', 'LX', '-', '3 Series', '2', 'Matiz', 'Focus', 'Attrage', 'Cayenne', 'Jolie', 'Captiva', 'Getz', 'ZS', 'Carens', 'Navara', 'Creta', 'Soluto', 'Escape', 'Hilux', 'Forte', 'XL7', 'Veloz', 'ES', 'Carnival', 'Khác', 'Rio', 'CX8', 'Zace', 'Pajero Sport', 'Swift', 'Wigo', 'Kona', '7 Series', 'Gentra', 'Rondo', 'Range Rover Evoque', 'Super Carry Truck', 'Macan', 'Panamera', 'Fiesta', 'GX', 'Dmax', '3008', 'Frontier', 'Carry', 'Porter', 'Aveo', 'Avanza', 'Accord', 'Almera', 'Sonet', 'Tiguan', 'X5', 'Hiace', 'G class', 'Avante', 'Raize', 'Super Carry Van', 'Colorado', 'Cooper', 'GLS', 'Ertiga', 'Laser', 'Sienna', 'Brio', 'Rush', 'HS', 'VF e34', 'Corolla', 'Mondeo', 'XC90', 'Q7', '5', 'NX', 'Grandis', 'Sedona', 'QKR', 'Maybach', 'cx3', 'Forester', 'Pajero', 'X6', 'LS', 'i20', 'Sunny', 'XC60', 'Optima', '5008', 'Nubira', 'K3000S', 'Towner', 'MU-X', 'County', 'GLE Class', 'GLB', '323', 'Lanos', 'GL', 'X trail', 'Orlando', 'Wrangler', 'Mighty', 'V class', 'X1', 'Polo', 'Grand Starex', 'Range Rover Sport', 'HD', 'CLA class', 'Q5', 'HRV', 'Venza', 'CX 30', 'Spectra', 'Vivant', '2008', 'Sonata', 'Teana', 'A4', '626', 'A6', 'X4', 'K5', 'Sprinter', 'Ciaz', 'VF9', 'Jazz', 'Flying Spur', 'X7', 'GLK Class', 'Hi lander', 'i30', 'Pride', 'X3', 'VF8', 'Z4', 'GLA class', 'F150', 'RAV4', 'Zinger', 'Levante', 'Phantom', 'XC40', 'Vitara', 'Teramont', 'K2700', 'Ghost', 'Magnus', 'Starex', 'MDX', '4 Series', 'Citivan', '718', 'Alphard', 'Verna', 'Lancer', 'IS', 'Mulsanne', 'Cressida', 'Passat', 'Mirage', 'Siena', 'A8', 'Grand livina', 'Ollin', 'Celerio', 'Tourneo', 'Picanto', 'Forland', 'Musso', 'Sportage', 'Libero', 'A class', 'Solati', 'Terra', 'APV', 'Range Rover Velar', 'Crown', 'Corona', 'Discovery Sport', 'Ghibli', 'DB1021', 'DB X30', '911', 'Highlander', 'Outback', 'President', 'Genesis', 'Bentayga', 'Trailblazer', 'GS', 'Mustang', 'S90', 'Defender', 'Escalade', 'QX', 'Foton', 'XJ series', 'Tundra', 'Bongo', 'NQR', 'A5', 'NPR', 'Veloster', 'Quattroporte', 'One', 'Cullinan', 'Trooper', 'Terios', 'Juke', 'Q3', 'Universe', 'MB', 'Traveller']
_BRANCH = ['Toyota', 'Hyundai', 'Kia', 'Ford', 'Mercedes Benz', 'Mazda', 'Honda', 'Mitsubishi', 'VinFast', 'Chevrolet', 'Lexus', 'BMW', 'Daewoo', 'Suzuki', 'Nissan', 'Porsche', 'LandRover', 'Isuzu', 'MG', 'Audi', 'Peugeot', 'Volkswagen', 'Hãng khác', 'Volvo', 'Thaco', 'Mini', 'Subaru', 'Bentley', 'Rolls Royce', 'Maserati', 'Jeep', 'Ssangyong', 'Daihatsu', 'Dongben', 'Fiat', 'Jaguar', 'Acura', 'Infiniti', 'Vinaxuki', 'Cadillac', 'Lincoln', 'Chrysler', 'Baic', 'Renault', 'JRD', 'Lamborghini', 'Chery', 'Luxgen', 'SYM', 'RAM']

def norm_class(text: str) -> str:
    if text in _CLASS:
        return text
    else:
        return 'other'

def norm_branch(text: str) -> str:
    if text in _BRANCH:
        return text
    else:
        return 'other'

def norm_model(text: str) -> str:
    dict_model = {
        'Sedan':'Sedan',
        'SUV':'Sedan', 
        'Crossover':'Crossover', 
        'Bán tải / Pickup':'Pickup', 
        'Van/Minivan':'Minivan',
        'Hatchback':'Hatchback', 
        'Truck':'Truck', 
        'Convertible/Cabriolet':'Cabriolet', 
        'Coupe':'Coupe'
    }
    return dict_model[text]

def norm_driver(text: str) -> str:
    dict_driver = {
        'RFD - Dẫn động cầu sau':'RFD',
        'AWD - 4 bánh toàn thời gian':'AWD', 
        'FWD - Dẫn động cầu trước':'FWD', 
        '4WD - Dẫn động 4 bánh':'4WD', 
    }
    return dict_driver[text]

def norm_km(text: str) -> int:
    return int(text.split('Km')[0].strip().replace(',',""))

def norm_status(text: str) -> str:
    dict_norm = {
        'Xe mới' : 'new',
        'Xe đã dùng' : 'old'
    }   
    return dict_norm[text]

def norm_origin(text: str) -> str:
    dict_origin = {
        'Lắp ráp trong nước' : 'domestic',
        'Nhập khẩu' : 'imported',
        'nhập khẩu': 'imported',
    }   
    return dict_origin[text]

def norm_fuel(text: str) -> str:
    if 'Xăng' in text:
        return 'gasoline'
    if 'Dầu' in text:
        return 'diesel'
    else:
        return 'diesel'

def norm_gearbox(text: str) -> str:
    dict_gearbox = {
        'Số tự động' : 'automatic',
        'Số tay' : 'manual',
    }   
    return dict_gearbox[text]