import requests
import time
from bs4 import BeautifulSoup
from dataclasses import dataclass
from random import randint
import csv

HOST = 'https://en.autoplius.lt'
USED_CARS_URL = HOST + '/ads/used-cars/'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


@dataclass
class Post:
    id: str
    make: str
    model: str
    manufacture_date: str
    mileage: str
    engine: str
    fuel_type: str
    driven_wheels: str
    gearbox: str
    seats_number: str
    wheel_size: str
    euro_standard: str
    comment: str
    mot_test_expiry: str
    steering_wheel: str
    climate_control: str
    first_registration_country: str
    seller_location: str
    seller_name: str
    price: str
    price_currency: str
    url: str
    immobilizer: int
    alarm: int
    satellite_tracking_system: int
    armoured: int
    cd_player: int
    mp3_player: int
    additional_audio_equipment: int
    cd_changer: int
    aux_input: int
    subwoofer: int
    dvd_player: int
    usb_input: int
    hands_free_kit: int
    apple_car_play_android_auto: int
    light_alloy_rims: int
    led_daytime_running_lights: int
    led_headlights: int
    xenon_lights: int
    fog_lights: int
    tow_hook: int
    headlights_washers: int
    roof_racks: int
    automatic_folding_mirrors: int
    set_of_winter_tyres: int
    electric_mirrors: int
    electric_boot_lid: int
    automatic_headlamps: int
    onboard_computer: int
    electrically_adjustable_steering_wheel: int
    rainfall_sensor: int
    heated_mirrors: int
    parking_sensors: int
    keyless_entry_system: int
    cruise_control: int
    heated_windshield: int
    start_stop_system: int
    voice_commands: int
    paddle_shifters: int
    lcd_monitor: int
    navigation_gps: int
    sport_seats: int
    tinted_windows: int
    multifunctional_steering_wheel: int
    heated_seats: int
    leather_seats: int
    sunroof: int
    electric_seats: int
    panoramic_roof: int
    auxiliary_heating: int
    ventilated_seats: int
    electric_seats_with_memory: int
    boot_cover: int
    heated_steering_wheel: int
    traction_control_system: int
    esp: int
    hill_start_assist_control: int
    automated_parking: int
    adaptive_cruise_control: int
    blind_spot_detection: int
    lane_departure_warning: int
    night_vision_assist: int
    road_sign_recognition: int
    isofix_mounts: int
    collision_prevention_assist: int
    high_beam_assist: int
    dynamic_cornering_lights: int
    back_view_camera: int
    front_view_camera: int
    three_six_zero_degree_camera: int
    spoilers: int
    increased_engine_power: int
    tuned_suspension: int
    tuned_interior: int
    prepared_for_motorsport: int
    not_exploited_in_lithuania: int
    imported_from_us: int
    for_exchange: int
    available_for_leasing: int
    service_book: int
    warranty: int
    catalytic_converter: int
    multiple_key_sets: int
    double_wheels: int
    folding_seats: int
    insulated_glass: int
    two_sliding_doors: int
    personal_ventilation: int
    personal_illumination: int


def get_soup(url):
    response = requests.get(url,
                            headers=HEADERS)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    return soup


def process_cars_detail_page(url):
    print('%s Processing detail page: %s' % (('#' * 4), url))

    soup = get_soup(url)

    if not soup:
        print('Detail. Soup is empty for url: %s' % url)
        return None

    post_id = soup.find(name='li', attrs={'class': 'announcement-id'})
    post_id = post_id.get_text(strip=True).replace('ID:', '').strip()

    crumbs = soup.find_all(name='li', attrs={'class': 'crumb'})
    make = crumbs[-2].get_text(strip=True)
    model = crumbs[-1].get_text(strip=True)

    parameters = {}

    for param in soup.find_all(name='div', attrs={'class': 'parameter-row'}):
        label_value = param.findChildren()
        if len(label_value) != 2 or label_value[0]['class'] != ['parameter-label'] or label_value[1]['class'] != ['parameter-value']:
            continue

        param_label = label_value[0].get_text(strip=True)
        param_value = label_value[1].get_text(strip=True)
        if param_label and param_value:
            parameters[param_label] = param_value

    seller_name = soup.find(name='div', attrs={'class': 'seller-contact-name'})
    seller_location = soup.find(name='div', attrs={'class': 'seller-contact-location'})
    price = soup.find(name='div', attrs={'class': 'price'})
    price_currency = soup.find(name='span', attrs={'class': 'default-currency'})
    comment = soup.find(name='div', attrs={'class': 'announcement-description'})

    if seller_name:
        seller_name = seller_name.get_text(strip=True)

    if seller_location:
        seller_location = seller_location.get_text(strip=True)

    if price:
        price = price.contents[0].strip()

    if price_currency:
        price_currency = price_currency.get_text(strip=True)

    if comment:
        comment = comment.get_text(strip=True)

    features = {}

    for feature in soup.find_all(name='div', attrs={'class': 'feature-list'}):
        feature_values = feature.findChildren('span', attrs={'class': 'feature-item'})
        for feature_item in feature_values:
            features[feature_item.get_text(strip=True)] = 1

    return Post(id=post_id,
                make=make,
                model=model,
                manufacture_date=parameters.get('Date of manufacture', None),
                mileage=parameters.get('Mileage', None),
                engine=parameters.get('Engine', None),
                fuel_type=parameters.get('Fuel type', None),
                driven_wheels=parameters.get('Driven wheels', None),
                gearbox=parameters.get('Gearbox', None),
                seats_number=parameters.get('Number of seats', None),
                climate_control=parameters.get('Climate control', None),
                steering_wheel=parameters.get('Steering wheel', None),
                wheel_size=parameters.get('Wheel size', None),
                euro_standard=parameters.get('Euro standard', None),
                first_registration_country=parameters.get('First registration country', None),
                comment=comment,
                mot_test_expiry=parameters.get('MOT test expiry', None),
                seller_location=seller_location,
                seller_name=seller_name,
                price=price,
                price_currency=price_currency,
                url=url,
                immobilizer=features.get('Immobilizer', 0),
                alarm=features.get('Alarm', 0),
                satellite_tracking_system=features.get('Satellite tracking system', 0),
                armoured=features.get('Armoured', 0),
                cd_player=features.get('CD player', 0),
                mp3_player=features.get('MP3 player', 0),
                additional_audio_equipment=features.get('Additional audio equipment', 0),
                cd_changer=features.get('CD changer', 0),
                aux_input=features.get('AUX input', 0),
                subwoofer=features.get('Subwoofer', 0),
                dvd_player=features.get('DVD player', 0),
                usb_input=features.get('USB input', 0),
                hands_free_kit=features.get('Handsfree kit', 0),
                apple_car_play_android_auto=features.get('Apple CarPlay / Android Auto', 0),
                light_alloy_rims=features.get('Light alloy rims', 0),
                led_daytime_running_lights=features.get('LED daytime running lights', 0),
                led_headlights=features.get('LED headlights', 0),
                xenon_lights=features.get('Xenon lights', 0),
                fog_lights=features.get('Fog lights', 0),
                tow_hook=features.get('Tow hook', 0),
                headlights_washers=features.get('Headlights washers', 0),
                roof_racks=features.get('Roof racks', 0),
                automatic_folding_mirrors=features.get('Automatic folding mirrors', 0),
                set_of_winter_tyres=features.get('Set of winter tyres', 0),
                electric_mirrors=features.get('Electric mirrors', 0),
                electric_boot_lid=features.get('Electric boot lid', 0),
                automatic_headlamps=features.get('Automatic headlamps', 0),
                onboard_computer=features.get('On-board computer', 0),
                electrically_adjustable_steering_wheel=features.get('Electrically adjustable steering wheel', 0),
                rainfall_sensor=features.get('Rainfall sensor', 0),
                heated_mirrors=features.get('Heated mirrors', 0),
                parking_sensors=features.get('Parking sensors', 0),
                keyless_entry_system=features.get('Keyless entry system', 0),
                cruise_control=features.get('Cruise control', 0),
                heated_windshield=features.get('Heated windshield', 0),
                start_stop_system=features.get('Start-Stop system', 0),
                voice_commands=features.get('Voice commands', 0),
                paddle_shifters=features.get('Paddle shifters', 0),
                lcd_monitor=features.get('LCD monitor', 0),
                navigation_gps=features.get('Navigation/GPS', 0),
                sport_seats=features.get('Sport seats', 0),
                tinted_windows=features.get('Tinted windows', 0),
                multifunctional_steering_wheel=features.get('Multifunctional steering wheel', 0),
                heated_seats=features.get('Heated seats', 0),
                leather_seats=features.get('Leather seats', 0),
                sunroof=features.get('Sunroof', 0),
                electric_seats=features.get('Electric seats', 0),
                panoramic_roof=features.get('Panoramic roof', 0),
                auxiliary_heating=features.get('Auxiliary heating', 0),
                ventilated_seats=features.get('Ventilated seats', 0),
                electric_seats_with_memory=features.get('Electric seats with memory', 0),
                boot_cover=features.get('Boot cover', 0),
                heated_steering_wheel=features.get('Heated steering wheel', 0),
                traction_control_system=features.get('Traction control system', 0),
                esp=features.get('ESP', 0),
                hill_start_assist_control=features.get('Hill-start assist control', 0),
                automated_parking=features.get('Automated Parking', 0),
                adaptive_cruise_control=features.get('Adaptive Cruise Control', 0),
                blind_spot_detection=features.get('Blind Spot Detection', 0),
                lane_departure_warning=features.get('Lane Departure Warning', 0),
                night_vision_assist=features.get('Night vision assist', 0),
                road_sign_recognition=features.get('Road sign recognition', 0),
                isofix_mounts=features.get('ISOFIX mounts', 0),
                collision_prevention_assist=features.get('Collision prevention assist', 0),
                high_beam_assist=features.get('High beam assist', 0),
                dynamic_cornering_lights=features.get('Dynamic cornering lights', 0),
                back_view_camera=features.get('Galinio vaizdo kamera', 0),
                front_view_camera=features.get('Front view camera', 0),
                three_six_zero_degree_camera=features.get('360° degree camera', 0),
                spoilers=features.get('Spoilers', 0),
                increased_engine_power=features.get('Increased engine power', 0),
                tuned_suspension=features.get('Tuned suspension', 0),
                tuned_interior=features.get('Tuned interior', 0),
                prepared_for_motorsport=features.get('Prepared for motorsport', 0),
                not_exploited_in_lithuania=features.get('Not exploited in Lithuania', 0),
                imported_from_us=features.get('Imported from US', 0),
                for_exchange=features.get('For exchange', 0),
                available_for_leasing=features.get('Available for leasing', 0),
                service_book=features.get('Service book', 0),
                warranty=features.get('Warranty', 0),
                catalytic_converter=features.get('Catalytic converter', 0),
                multiple_key_sets=features.get('Multiple key sets', 0),
                double_wheels=features.get('Double wheels', 0),
                folding_seats=features.get('Atlenkiamos Sėdynės', 0),
                insulated_glass=features.get('Insulated glass', 0),
                two_sliding_doors=features.get('Two sliding doors', 0),
                personal_ventilation=features.get('Personal ventilation', 0),
                personal_illumination=features.get('Personal illumination', 0))


def process_cars_list_page(soup):
    for post in soup.find_all(name='a', attrs={'class': 'announcement-item'}):
        time.sleep(randint(1, 3))
        yield process_cars_detail_page(post['href'])


def get_next_url(soup):
    next_page = soup.find(name='a', attrs={'class': 'next',
                                           'rel': 'next'})
    if not next_page:
        return None

    parent_next_page = next_page.find_parent(name='li', attrs={'class': 'next'})

    if parent_next_page:
        return HOST + next_page['href']
    return None


def main():
    next_url = USED_CARS_URL
    data = []

    while next_url:
        try:
            print('Processing list page: %s' % next_url)

            soup = get_soup(next_url)

            if not soup:
                print('List. Soup is empty for url: %s' % next_url)
                break

            for item in process_cars_list_page(soup):
                data.append(item)

            next_url = get_next_url(soup)
            time.sleep(randint(1, 3))
        except KeyboardInterrupt:
            break

    keys = data[0].keys()
    with open('data.csv', 'w+') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


if __name__ == '__main__':
    main()
