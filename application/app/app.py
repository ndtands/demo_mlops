import requests
import json
import streamlit as st

def decode(price: int) -> str:
    bilion = price//1000
    milion = price%1000
    if bilion > 0:
        return f"{bilion} tỉ {milion} triệu VND"
    else:
        return f"{milion} triệu VND"
        
st.title("The price of used cars App")
st.sidebar.title("Features")

year_manufacture = st.sidebar.text_input('Year of Manufacture', 2020)
_CLASS = sorted(['Ranger', 'Morning', 'Vios', 'Innova', 'Camry', 'C class', 'i10', 'Fortuner', 'SantaFe', 'E class', '3', 'GLC', 'Everest', 'Accent', 'CX5', 'Corolla altis', 'CRV', 'Lux A 2.0', 'S class', 'Cerato', 'Spark', 'RX', 'Tucson', 'City', 'Civic', 'Fadil', 'Xpander', 'Elantra', 'Lux SA 2.0', 'Corolla Cross', 'Yaris', 'Lacetti', 'Cruze', 'Transit', '6', 'Explorer', 'EcoSport', 'Prado', 'K3', 'Triton', 'Sorento', '5 Series', 'Range Rover', 'Outlander', 'Land Cruiser', 'BT50', 'Seltos', 'LX', '-', '3 Series', '2', 'Matiz', 'Focus', 'Attrage', 'Cayenne', 'Jolie', 'Captiva', 'Getz', 'ZS', 'Carens', 'Navara', 'Creta', 'Soluto', 'Escape', 'Hilux', 'Forte', 'XL7', 'Veloz', 'ES', 'Carnival', 'Khác', 'Rio', 'CX8', 'Zace', 'Pajero Sport', 'Swift', 'Wigo', 'Kona', '7 Series', 'Gentra', 'Rondo', 'Range Rover Evoque', 'Super Carry Truck', 'Macan', 'Panamera', 'Fiesta', 'GX', 'Dmax', '3008', 'Frontier', 'Carry', 'Porter', 'Aveo', 'Avanza', 'Accord', 'Almera', 'Sonet', 'Tiguan', 'X5', 'Hiace', 'G class', 'Avante', 'Raize', 'Super Carry Van', 'Colorado', 'Cooper', 'GLS', 'Ertiga', 'Laser', 'Sienna', 'Brio', 'Rush', 'HS', 'VF e34', 'Corolla', 'Mondeo', 'XC90', 'Q7', '5', 'NX', 'Grandis', 'Sedona', 'QKR', 'Maybach', 'cx3', 'Forester', 'Pajero', 'X6', 'LS', 'i20', 'Sunny', 'XC60', 'Optima', '5008', 'Nubira', 'K3000S', 'Towner', 'MU-X', 'County', 'GLE Class', 'GLB', '323', 'Lanos', 'GL', 'X trail', 'Orlando', 'Wrangler', 'Mighty', 'V class', 'X1', 'Polo', 'Grand Starex', 'Range Rover Sport', 'HD', 'CLA class', 'Q5', 'HRV', 'Venza', 'CX 30', 'Spectra', 'Vivant', '2008', 'Sonata', 'Teana', 'A4', '626', 'A6', 'X4', 'K5', 'Sprinter', 'Ciaz', 'VF9', 'Jazz', 'Flying Spur', 'X7', 'GLK Class', 'Hi lander', 'i30', 'Pride', 'X3', 'VF8', 'Z4', 'GLA class', 'F150', 'RAV4', 'Zinger', 'Levante', 'Phantom', 'XC40', 'Vitara', 'Teramont', 'K2700', 'Ghost', 'Magnus', 'Starex', 'MDX', '4 Series', 'Citivan', '718', 'Alphard', 'Verna', 'Lancer', 'IS', 'Mulsanne', 'Cressida', 'Passat', 'Mirage', 'Siena', 'A8', 'Grand livina', 'Ollin', 'Celerio', 'Tourneo', 'Picanto', 'Forland', 'Musso', 'Sportage', 'Libero', 'A class', 'Solati', 'Terra', 'APV', 'Range Rover Velar', 'Crown', 'Corona', 'Discovery Sport', 'Ghibli', 'DB1021', 'DB X30', '911', 'Highlander', 'Outback', 'President', 'Genesis', 'Bentayga', 'Trailblazer', 'GS', 'Mustang', 'S90', 'Defender', 'Escalade', 'QX', 'Foton', 'XJ series', 'Tundra', 'Bongo', 'NQR', 'A5', 'NPR', 'Veloster', 'Quattroporte', 'One', 'Cullinan', 'Trooper', 'Terios', 'Juke', 'Q3', 'Universe', 'MB', 'Traveller','other'])
_BRANCH = sorted(['Toyota', 'Hyundai', 'Kia', 'Ford', 'Mercedes Benz', 'Mazda', 'Honda', 'Mitsubishi', 'VinFast', 'Chevrolet', 'Lexus', 'BMW', 'Daewoo', 'Suzuki', 'Nissan', 'Porsche', 'LandRover', 'Isuzu', 'MG', 'Audi', 'Peugeot', 'Volkswagen', 'Hãng khác', 'Volvo', 'Thaco', 'Mini', 'Subaru', 'Bentley', 'Rolls Royce', 'Maserati', 'Jeep', 'Ssangyong', 'Daihatsu', 'Dongben', 'Fiat', 'Jaguar', 'Acura', 'Infiniti', 'Vinaxuki', 'Cadillac', 'Lincoln', 'Chrysler', 'Baic', 'Renault', 'JRD', 'Lamborghini', 'Chery', 'Luxgen','RAM','other'])

branch = st.sidebar.selectbox(label='Branch', options=_BRANCH, index=6)
_class = st.sidebar.selectbox(label='Class', options=_CLASS, index=6)
# if branch == 'Honda':
#     model_list = ['Accord', 'Brio', 'CRV', 'City', 'Civic', 'HRV', 'Jazz', 'Odyssey', 'Pilot']
#     model = st.sidebar.selectbox(label='Model', options=model_list, index=2)
# else:
#     model = st.text_input('Model', 'CRV')

km = st.sidebar.slider(label='Km Driven', value=10000, min_value=0, max_value=200000)
num_seat = st.sidebar.slider(label='#Seats', value=5, min_value=2, max_value=16)
num_door = st.sidebar.slider(label='#Doors', value=5, min_value=2, max_value=16)

origin_list = ['domestic', 'imported']
origin = st.sidebar.selectbox(label='Origin', options=origin_list, index=0)

color_exterior_list = sorted(['Bạc', 'Cam', 'Cát', 'Ghi', 'Hồng', 'Kem', 'Màu khác', 'Nhiều màu', 'Nâu', 'Trắng', 'Tím', 'Vàng', 'Xanh', 'Xám', 'Đen', 'Đỏ', 'Đồng'])
color_furniture_list = sorted(['Bạc', 'Cam', 'Cát', 'Ghi', 'Hồng', 'Kem', 'Màu khác', 'Nhiều màu', 'Nâu', 'Trắng', 'Tím', 'Vàng', 'Xanh', 'Xám', 'Đen', 'Đỏ', 'Đồng'])

color_exterior = st.sidebar.selectbox(label='Internal Color', options=color_exterior_list, index=14)
color_furniture = st.sidebar.selectbox(label='External Color', options=color_furniture_list, index=9)

gear_box_list = ['automatic', 'manual']
gearbox = st.sidebar.selectbox(label='Gear box', options=gear_box_list)

wheel_drive_list = ['4WD', 'AWD', 'FWD', 'RWD']
driver = st.sidebar.selectbox(label='Wheel Drive', options=wheel_drive_list, index=3)

model_list = ['Sedan', 'Crossover', 'Pickup', 'Minivan', 'Hatchback', 'Cabriolet', 'Coupe','Truck']
model = st.sidebar.selectbox(label='Car Type', options=model_list, index=6)

is_predict = st.button('Click here to predict')

if is_predict:
    predict_api = 'http://localhost:8010/api/predict'
    data = {'year_manufacture': int(year_manufacture),
            'km': km,
            'num_seat': num_seat,
            'num_door': num_door,
            'branch': branch,
            'class_': _class,
            'origin': origin,
            'color_exterior': color_exterior,
            'color_furniture': color_furniture,
            'gearbox': gearbox,
            'driver': driver,
            'model': model,
           }

    print(json.dumps(data))
    response = requests.post(url=predict_api, data=json.dumps(data))
    content = json.loads(response.content)
    results = content['price']

    st.text(decode(int(results)))
    st.image('./stores/sample.jpg')