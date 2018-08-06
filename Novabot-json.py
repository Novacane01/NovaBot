from random import randint
from slackclient import SlackClient
import urllib.request
import json
import requests
import psycopg2
import random
from urllib import parse


class NovaBot():
    client = SlackClient("xoxb-301260605360-h3vtlrydfMDGddbtSFygE1i5")
    client2 = SlackClient('xoxp-301325579249-301896473906-302029170469-4a92e4f6cf89406f8071270942637854')
    webhook_url = 'https://hooks.slack.com/services/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'
    url = parse.urlparse(
        "postgres://pkqqrhksxqhexa:4be7a6fb4d46a30a04867aed7093ab678230db93ef9b7f885d6068c701316b7c@ec2-107-21-201-57.compute-1.amazonaws.com:5432/d6evup307rbj4q")
    currentuser = None
    previoususer = None
    responding = False
    message = ""
    response = ""
    previous_ts = None
    reacted = False
    matched = False
    slackusers = ['U8VSCDXSN', 'U8VSDD92N', 'UA8FX19B7', 'U8W1947MK', 'U9412JUTV', 'U8VFC1LAV', 'U8VV71VFF',
                  'U8V9P141X', 'U8VRS7750', 'U8WTSSFFZ', 'U8VSUPEKE', 'U8W6SMRPX', 'U8VQ0DG7M']
    reactions = ['hash', 'keycap_star', 'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'copyright', 'registered', 'mahjong', 'black_joker', 'a', 'b', 'o2', 'parking', 'ab', 'cl', 'cool', 'free', 'id', 'new', 'ng', 'ok', 'sos', 'up', 'vs', 'koko', 'sa', 'u7121', 'u6307', 'u7981', 'u7a7a', 'u5408', 'u6e80', 'u6709', 'u6708', 'u7533', 'u5272', 'u55b6', 'ideograph_advantage', 'accept', 'cyclone', 'foggy', 'closed_umbrella', 'night_with_stars', 'sunrise_over_mountains', 'sunrise', 'city_sunset', 'city_sunrise', 'rainbow', 'bridge_at_night', 'ocean', 'volcano', 'milky_way', 'earth_africa', 'earth_americas', 'earth_asia', 'globe_with_meridians', 'new_moon', 'waxing_crescent_moon', 'first_quarter_moon', 'full_moon', 'waning_gibbous_moon', 'last_quarter_moon', 'waning_crescent_moon', 'crescent_moon', 'new_moon_with_face', 'first_quarter_moon_with_face', 'last_quarter_moon_with_face', 'full_moon_with_face', 'sun_with_face', 'star2', 'stars', 'thermometer', 'rain_cloud', 'snow_cloud', 'fog', 'wind_blowing_face', 'hotdog', 'taco', 'burrito', 'chestnut', 'seedling', 'evergreen_tree', 'deciduous_tree', 'palm_tree', 'cactus', 'hot_pepper', 'tulip', 'cherry_blossom', 'rose', 'hibiscus', 'sunflower', 'blossom', 'corn', 'ear_of_rice', 'herb', 'four_leaf_clover', 'maple_leaf', 'fallen_leaf', 'leaves', 'mushroom', 'tomato', 'eggplant', 'grapes', 'melon', 'watermelon', 'tangerine', 'lemon', 'banana', 'pineapple', 'apple', 'green_apple', 'pear', 'peach', 'cherries', 'strawberry', 'hamburger', 'pizza', 'meat_on_bone', 'poultry_leg', 'rice_cracker', 'rice_ball', 'rice', 'curry', 'ramen', 'spaghetti', 'bread', 'fries', 'sweet_potato', 'dango', 'oden', 'sushi', 'fried_shrimp', 'fish_cake', 'icecream', 'shaved_ice', 'ice_cream', 'doughnut', 'cookie', 'chocolate_bar', 'candy', 'lollipop', 'custard', 'honey_pot', 'cake', 'bento', 'stew', 'fork_and_knife', 'tea', 'sake', 'wine_glass', 'cocktail', 'tropical_drink', 'beer', 'beers', 'baby_bottle', 'knife_fork_plate', 'champagne', 'popcorn', 'ribbon', 'gift', 'birthday', 'jack_o_lantern', 'christmas_tree', 'santa', 'fireworks', 'sparkler', 'balloon', 'tada', 'confetti_ball', 'tanabata_tree', 'crossed_flags', 'bamboo', 'dolls', 'flags', 'wind_chime', 'rice_scene', 'school_satchel', 'mortar_board', 'medal', 'reminder_ribbon', 'studio_microphone', 'level_slider', 'control_knobs', 'film_frames', 'admission_tickets', 'carousel_horse', 'ferris_wheel', 'roller_coaster', 'fishing_pole_and_fish', 'microphone', 'movie_camera', 'cinema', 'headphones', 'art', 'tophat', 'circus_tent', 'ticket', 'clapper', 'performing_arts', 'video_game', 'dart', 'slot_machine', '8ball', 'game_die', 'bowling', 'flower_playing_cards', 'musical_note', 'notes', 'saxophone', 'guitar', 'musical_keyboard', 'trumpet', 'violin', 'musical_score', 'running_shirt_with_sash', 'tennis', 'ski', 'basketball', 'checkered_flag', 'snowboarder', 'surfer', 'sports_medal', 'trophy', 'horse_racing', 'football', 'rugby_football', 'swimmer', 'weight_lifter', 'golfer', 'racing_motorcycle', 'racing_car', 'cricket_bat_and_ball', 'volleyball', 'field_hockey_stick_and_ball', 'ice_hockey_stick_and_puck', 'table_tennis_paddle_and_ball', 'snow_capped_mountain', 'camping', 'beach_with_umbrella', 'building_construction', 'house_buildings', 'cityscape', 'derelict_house_building', 'classical_building', 'desert', 'desert_island', 'national_park', 'stadium', 'house', 'house_with_garden', 'office', 'post_office', 'european_post_office', 'hospital', 'bank', 'atm', 'hotel', 'love_hotel', 'convenience_store', 'school', 'department_store', 'factory', 'japanese_castle', 'european_castle', 'waving_white_flag', 'waving_black_flag', 'rosette', 'label', 'badminton_racquet_and_shuttlecock', 'bow_and_arrow', 'amphora', 'rat', 'mouse2', 'ox', 'water_buffalo', 'cow2', 'tiger2', 'leopard', 'rabbit2', 'cat2', 'dragon', 'crocodile', 'whale2', 'snail', 'snake', 'racehorse', 'ram', 'goat', 'sheep', 'monkey', 'rooster', 'chicken', 'dog2', 'pig2', 'boar', 'elephant', 'octopus', 'shell', 'bug', 'ant', 'beetle', 'fish', 'tropical_fish', 'blowfish', 'turtle', 'hatching_chick', 'baby_chick', 'hatched_chick', 'bird', 'penguin', 'koala', 'poodle', 'dromedary_camel', 'camel', 'mouse', 'cow', 'tiger', 'rabbit', 'cat', 'dragon_face', 'whale', 'horse', 'monkey_face', 'dog', 'pig', 'frog', 'hamster', 'wolf', 'bear', 'panda_face', 'pig_nose', 'chipmunk', 'eyes', 'eye', 'ear', 'nose', 'lips', 'tongue', 'point_up_2', 'point_down', 'point_left', 'point_right', 'wave', 'ok_hand', 'clap', 'open_hands', 'crown', 'womans_hat', 'eyeglasses', 'necktie', 'jeans', 'dress', 'kimono', 'bikini', 'womans_clothes', 'purse', 'handbag', 'pouch', 'athletic_shoe', 'high_heel', 'sandal', 'boot', 'footprints', 'bust_in_silhouette', 'busts_in_silhouette', 'boy', 'girl', 'man', 'woman', 'two_men_holding_hands', 'two_women_holding_hands', 'cop', 'dancers', 'bride_with_veil', 'person_with_blond_hair', 'man_with_gua_pi_mao', 'man_with_turban', 'older_man', 'older_woman', 'baby', 'construction_worker', 'princess', 'japanese_ogre', 'japanese_goblin', 'ghost', 'angel', 'alien', 'space_invader', 'imp', 'skull', 'information_desk_person', 'guardsman', 'dancer', 'lipstick', 'nail_care', 'massage', 'haircut', 'barber', 'syringe', 'pill', 'kiss', 'love_letter', 'ring', 'gem', 'couplekiss', 'bouquet', 'couple_with_heart', 'wedding', 'heartbeat', 'broken_heart', 'two_hearts', 'sparkling_heart', 'heartpulse', 'cupid', 'blue_heart', 'green_heart', 'yellow_heart', 'purple_heart', 'gift_heart', 'revolving_hearts', 'heart_decoration', 'diamond_shape_with_a_dot_inside', 'bulb', 'anger', 'bomb', 'zzz', 'sweat_drops', 'droplet', 'dash', 'muscle', 'dizzy', 'speech_balloon', 'thought_balloon', 'white_flower', '100', 'moneybag', 'currency_exchange', 'heavy_dollar_sign', 'credit_card', 'yen', 'dollar', 'euro', 'pound', 'money_with_wings', 'chart', 'seat', 'computer', 'briefcase', 'minidisc', 'floppy_disk', 'cd', 'dvd', 'file_folder', 'open_file_folder', 'page_with_curl', 'page_facing_up', 'date', 'calendar', 'card_index', 'chart_with_upwards_trend', 'chart_with_downwards_trend', 'bar_chart', 'clipboard', 'pushpin', 'round_pushpin', 'paperclip', 'straight_ruler', 'triangular_ruler', 'bookmark_tabs', 'ledger', 'notebook', 'notebook_with_decorative_cover', 'closed_book', 'green_book', 'blue_book', 'orange_book', 'books', 'name_badge', 'scroll', 'telephone_receiver', 'pager', 'fax', 'satellite_antenna', 'loudspeaker', 'mega', 'outbox_tray', 'inbox_tray', 'package', 'incoming_envelope', 'envelope_with_arrow', 'mailbox_closed', 'mailbox', 'mailbox_with_mail', 'mailbox_with_no_mail', 'postbox', 'postal_horn', 'newspaper', 'iphone', 'calling', 'vibration_mode', 'mobile_phone_off', 'no_mobile_phones', 'signal_strength', 'camera', 'camera_with_flash', 'video_camera', 'tv', 'radio', 'vhs', 'film_projector', 'prayer_beads', 'twisted_rightwards_arrows', 'repeat', 'repeat_one', 'arrows_clockwise', 'arrows_counterclockwise', 'low_brightness', 'high_brightness', 'mute', 'speaker', 'sound', 'loud_sound', 'battery', 'electric_plug', 'mag', 'mag_right', 'lock_with_ink_pen', 'closed_lock_with_key', 'key', 'lock', 'unlock', 'bell', 'no_bell', 'bookmark', 'link', 'radio_button', 'back', 'end', 'on', 'soon', 'top', 'underage', 'keycap_ten', 'capital_abcd', 'abcd', '1234', 'symbols', 'abc', 'fire', 'flashlight', 'wrench', 'hammer', 'nut_and_bolt', 'gun', 'microscope', 'telescope', 'crystal_ball', 'six_pointed_star', 'beginner', 'trident', 'black_square_button', 'white_square_button', 'red_circle', 'large_blue_circle', 'large_orange_diamond', 'large_blue_diamond', 'small_orange_diamond', 'small_blue_diamond', 'small_red_triangle', 'small_red_triangle_down', 'arrow_up_small', 'arrow_down_small', 'om_symbol', 'dove_of_peace', 'kaaba', 'mosque', 'synagogue', 'menorah_with_nine_branches', 'clock1', 'clock2', 'clock3', 'clock4', 'clock5', 'clock6', 'clock7', 'clock8', 'clock9', 'clock10', 'clock11', 'clock12', 'clock130', 'clock230', 'clock330', 'clock430', 'clock530', 'clock630', 'clock730', 'clock830', 'clock930', 'clock1030', 'clock1130', 'clock1230', 'candle', 'mantelpiece_clock', 'hole', 'man_in_business_suit_levitating', 'sleuth_or_spy', 'dark_sunglasses', 'spider', 'spider_web', 'joystick', 'man_dancing', 'linked_paperclips', 'lower_left_ballpoint_pen', 'lower_left_fountain_pen', 'lower_left_paintbrush', 'lower_left_crayon', 'raised_hand_with_fingers_splayed', 'black_heart', 'desktop_computer', 'printer', 'three_button_mouse', 'trackball', 'frame_with_picture', 'card_index_dividers', 'card_file_box', 'file_cabinet', 'wastebasket', 'spiral_note_pad', 'spiral_calendar_pad', 'compression', 'old_key', 'rolled_up_newspaper', 'dagger_knife', 'speaking_head_in_silhouette', 'left_speech_bubble', 'right_anger_bubble', 'ballot_box_with_ballot', 'world_map', 'mount_fuji', 'tokyo_tower', 'statue_of_liberty', 'japan', 'moyai', 'grinning', 'grin', 'joy', 'smiley', 'smile', 'sweat_smile', 'innocent', 'smiling_imp', 'wink', 'blush', 'yum', 'relieved', 'heart_eyes', 'sunglasses', 'smirk', 'neutral_face', 'expressionless', 'unamused', 'sweat', 'pensive', 'confused', 'confounded', 'kissing', 'kissing_heart', 'kissing_smiling_eyes', 'kissing_closed_eyes', 'stuck_out_tongue', 'stuck_out_tongue_winking_eye', 'stuck_out_tongue_closed_eyes', 'disappointed', 'worried', 'angry', 'rage', 'cry', 'persevere', 'triumph', 'disappointed_relieved', 'frowning', 'anguished', 'fearful', 'weary', 'sleepy', 'tired_face', 'grimacing', 'sob', 'open_mouth', 'hushed', 'cold_sweat', 'scream', 'astonished', 'flushed', 'sleeping', 'dizzy_face', 'no_mouth', 'mask', 'smile_cat', 'joy_cat', 'smiley_cat', 'heart_eyes_cat', 'smirk_cat', 'kissing_cat', 'pouting_cat', 'crying_cat_face', 'scream_cat', 'slightly_frowning_face', 'slightly_smiling_face', 'upside_down_face', 'face_with_rolling_eyes', 'no_good', 'ok_woman', 'bow', 'see_no_evil', 'hear_no_evil', 'speak_no_evil', 'raising_hand', 'raised_hands', 'person_frowning', 'person_with_pouting_face', 'pray', 'rocket', 'helicopter', 'steam_locomotive', 'railway_car', 'bullettrain_side', 'bullettrain_front', 'train2', 'metro', 'light_rail', 'station', 'tram', 'train', 'bus', 'oncoming_bus', 'trolleybus', 'busstop', 'minibus', 'ambulance', 'fire_engine', 'police_car', 'oncoming_police_car', 'taxi', 'oncoming_taxi', 'oncoming_automobile', 'blue_car', 'truck', 'articulated_lorry', 'tractor', 'monorail', 'mountain_railway', 'suspension_railway', 'mountain_cableway', 'aerial_tramway', 'ship', 'rowboat', 'speedboat', 'traffic_light', 'vertical_traffic_light', 'construction', 'rotating_light', 'triangular_flag_on_post', 'door', 'no_entry_sign', 'smoking', 'no_smoking', 'put_litter_in_its_place', 'do_not_litter', 'potable_water', 'bike', 'no_bicycles', 'bicyclist', 'mountain_bicyclist', 'walking', 'no_pedestrians', 'children_crossing', 'mens', 'womens', 'restroom', 'baby_symbol', 'toilet', 'wc', 'shower', 'bath', 'bathtub', 'passport_control', 'customs', 'baggage_claim', 'left_luggage', 'couch_and_lamp', 'sleeping_accommodation', 'shopping_bags', 'bellhop_bell', 'bed', 'place_of_worship', 'octagonal_sign', 'shopping_trolley', 'hammer_and_wrench', 'shield', 'oil_drum', 'motorway', 'railway_track', 'motor_boat', 'small_airplane', 'airplane_departure', 'airplane_arriving', 'satellite', 'passenger_ship', 'scooter', 'motor_scooter', 'canoe', 'sled', 'flying_saucer', 'zipper_mouth_face', 'money_mouth_face', 'face_with_thermometer', 'nerd_face', 'thinking_face', 'face_with_head_bandage', 'robot_face', 'hugging_face', 'call_me_hand', 'raised_back_of_hand', 'handshake', 'i_love_you_hand_sign', 'face_with_cowboy_hat', 'clown_face', 'nauseated_face', 'rolling_on_the_floor_laughing', 'drooling_face', 'lying_face', 'face_palm', 'sneezing_face', 'pregnant_woman', 'palms_up_together', 'selfie', 'prince', 'man_in_tuxedo', 'shrug', 'person_doing_cartwheel', 'juggling', 'fencer', 'wrestlers', 'water_polo', 'handball', 'wilted_flower', 'drum_with_drumsticks', 'clinking_glasses', 'tumbler_glass', 'spoon', 'goal_net', 'first_place_medal', 'second_place_medal', 'third_place_medal', 'boxing_glove', 'martial_arts_uniform', 'curling_stone', 'croissant', 'avocado', 'cucumber', 'bacon', 'potato', 'carrot', 'baguette_bread', 'green_salad', 'shallow_pan_of_food', 'stuffed_flatbread', 'egg', 'glass_of_milk', 'peanuts', 'kiwifruit', 'pancakes', 'dumpling', 'fortune_cookie', 'takeout_box', 'chopsticks', 'bowl_with_spoon', 'cup_with_straw', 'coconut', 'broccoli', 'pie', 'pretzel', 'cut_of_meat', 'sandwich', 'canned_food', 'crab', 'lion_face', 'scorpion', 'turkey', 'unicorn_face', 'eagle', 'duck', 'bat', 'shark', 'owl', 'fox_face', 'butterfly', 'deer', 'gorilla', 'lizard', 'rhinoceros', 'shrimp', 'squid', 'giraffe_face', 'zebra_face', 'hedgehog', 'sauropod', 'cricket', 'cheese_wedge', 'face_with_monocle', 'adult', 'child', 'older_adult', 'bearded_person', 'person_with_headscarf', 'woman_in_steamy_room', 'man_in_steamy_room', 'person_in_steamy_room', 'woman_climbing', 'man_climbing', 'person_climbing', 'woman_in_lotus_position', 'man_in_lotus_position', 'person_in_lotus_position', 'female_mage', 'male_mage', 'mage', 'female_fairy', 'male_fairy', 'fairy', 'female_vampire', 'male_vampire', 'vampire', 'mermaid', 'merman', 'merperson', 'female_elf', 'male_elf', 'elf', 'female_genie', 'male_genie', 'genie', 'female_zombie', 'male_zombie', 'zombie', 'brain', 'orange_heart', 'billed_cap', 'scarf', 'gloves', 'coat', 'socks', 'bangbang', 'interrobang', 'tm', 'information_source', 'left_right_arrow', 'arrow_up_down', 'arrow_upper_left', 'arrow_upper_right', 'arrow_lower_right', 'arrow_lower_left', 'leftwards_arrow_with_hook', 'arrow_right_hook', 'watch', 'hourglass', 'keyboard', 'eject', 'fast_forward', 'rewind', 'arrow_double_up', 'arrow_double_down', 'black_right_pointing_double_triangle_with_vertical_bar', 'black_left_pointing_double_triangle_with_vertical_bar', 'black_right_pointing_triangle_with_double_vertical_bar', 'alarm_clock', 'stopwatch', 'timer_clock', 'hourglass_flowing_sand', 'double_vertical_bar', 'black_square_for_stop', 'black_circle_for_record', 'm', 'black_small_square', 'white_small_square', 'arrow_forward', 'arrow_backward', 'white_medium_square', 'black_medium_square', 'white_medium_small_square', 'black_medium_small_square', 'sunny', 'cloud', 'umbrella', 'snowman', 'comet', 'ballot_box_with_check', 'umbrella_with_rain_drops', 'coffee', 'shamrock', 'point_up', 'skull_and_crossbones', 'radioactive_sign', 'biohazard_sign', 'orthodox_cross', 'star_and_crescent', 'peace_symbol', 'yin_yang', 'wheel_of_dharma', 'white_frowning_face', 'relaxed', 'female_sign', 'male_sign', 'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpius', 'sagittarius', 'capricorn', 'aquarius', 'pisces', 'spades', 'clubs', 'hearts', 'diamonds', 'hotsprings', 'recycle', 'wheelchair', 'hammer_and_pick', 'anchor', 'crossed_swords', 'scales', 'alembic', 'gear', 'atom_symbol', 'fleur_de_lis', 'warning', 'zap', 'white_circle', 'black_circle', 'coffin', 'funeral_urn', 'soccer', 'baseball', 'snowman_without_snow', 'partly_sunny', 'thunder_cloud_and_rain', 'ophiuchus', 'pick', 'helmet_with_white_cross', 'chains', 'no_entry', 'shinto_shrine', 'church', 'mountain', 'umbrella_on_ground', 'fountain', 'golf', 'ferry', 'skier', 'ice_skate', 'person_with_ball', 'tent', 'fuelpump', 'scissors', 'white_check_mark', 'airplane', 'fist', 'v', 'writing_hand', 'pencil2', 'black_nib', 'heavy_check_mark', 'heavy_multiplication_x', 'latin_cross', 'star_of_david', 'sparkles', 'eight_spoked_asterisk', 'eight_pointed_black_star', 'snowflake', 'sparkle', 'x', 'negative_squared_cross_mark', 'question', 'grey_question', 'grey_exclamation', 'heavy_heart_exclamation_mark_ornament', 'heart', 'heavy_plus_sign', 'heavy_minus_sign', 'heavy_division_sign', 'arrow_right', 'curly_loop', 'loop', 'arrow_heading_up', 'arrow_heading_down', 'arrow_left', 'arrow_up', 'arrow_down', 'black_large_square', 'white_large_square', 'star', 'o', 'wavy_dash', 'part_alternation_mark', 'congratulations', 'secret']

    def __init__(self):
        self.client.rtm_connect()
        my_user_name = self.client.server.username
        parse.uses_netloc.append("postgres")
        r = self.client2.api_call('emoji.list',None)
        for key in r['emoji']:
            self.reactions.append(key)
        #self.post('C8VNSRYTV',"Hey guys VSauce here")
        print("Connected to slack")

    def post(self, channel, msg):
        # self.client2.api_call('chat.postMessage',None,channel = channel,text = msg)
        chan = self.client.server.channels.find(channel)
        if not chan:
            raise Exception("Channel %s not found." % channel)
        return chan.send_message(msg)

    def postJson(self, jsonData):
        jsonDumps = json.dumps(jsonData)
        r = requests.post(self.webhook_url, data=jsonDumps, headers={'Content-Type': 'application/json'})
        print("Status Code:" + str(r.status_code) + "\nMessage Sent")

    def react(self, msg):
        if 'reaction' in msg:
            self.client.api_call("reactions.add", None, name=msg['reaction'],
                                 channel=msg['item']['channel'], timestamp=msg['item']['ts'])
        else:
            for word in msg["text"].split():
                for reaction in self.reactions:
                    if word == reaction:
                        self.client.api_call("reactions.add", None, name=reaction,
                                             channel=msg['channel'], timestamp=msg['ts'])

    def getreactions(self, msg):
        return self.client.api_call("reactions.get", None, channel=msg['item']['channel'], timestamp=msg['item']['ts'])

    def sendimg(self, msg):
        l = []
        msg['text'] = str(msg['text']).replace("!image ", "")
        req = urllib.request.Request('https://imgur.com/search/score?q={}'.format(msg['text']),
                                     headers={'User-Agent': 'Mozilla/5.0'})
        imgurl = urllib.request.urlopen(req)
        html = imgurl.read()
        for i in str(html).split():
            if '.jpg\"' in i and 'i.imgur.com' in i:
                i = i.replace("src=", "https:")
                i = i.replace("\"", "")
                l.append(i)
        try:
            self.post(msg['channel'], l[random.randint(0, len(l) - 1)])
            return
        except:
            return

    def getvid(self, msg):
        msg['text'] = str(msg['text']).replace("!video ", "")
        msg['text'] = str(msg['text']).replace(" ", "+")
        req = urllib.request.Request('https://www.youtube.com/results?search_query={}'.format(msg['text']),
                                     headers={'User-Agent': 'Mozilla/5.0'})
        vidurl = urllib.request.urlopen(req)
        html = vidurl.read()
        for i in str(html).split():
            if 'href=\"/watch' in i:
                i = i.replace("href=", "")
                i = i.replace("\"", "")
                try:
                    self.post(msg['channel'], "https://www.youtube.com" + i)
                    return
                except:
                    print("Video could not be found")
                    return

    def process_message(self, msg):
        # self.post({"text": "Gerard love my master"})
        if randint(0, 4) == 3:
            self.react(msg)
            print("Reacting")
        # if str(msg['text']).lower() == 'hello':
        #     jsonData = {"text": "Hello everybody in #general",
        #                 "attachments": [{"fallback": "Come have a blast at https://www.clubpenguinisland.com/",
        #                                  "actions": [{"type": "button", "text": "@Novacane",
        #                                               "url": "https://www.clubpenguinisland.com/"}]}]}
        #     self.postJson(jsonData)
        if '!video' in str(msg['text']).lower():
            self.getvid(msg)
        if "!image" in msg['text']:
            self.sendimg(msg)
        if "!gofuckyourself" in msg["text"]:
            self.post(msg['channel'],
                      '<@{}> go fuck yourself'.format(self.slackusers[randint(0, len(self.slackusers))]))
        conn = psycopg2.connect(
            database=self.url.path[1:],
            user=self.url.username,
            password=self.url.password,
            host=self.url.hostname,
            port=self.url.port
        )

        cursor = conn.cursor()

        if self.previoususer is None:
            self.previoususer = msg['user']
        if msg['user'] != self.previoususer and not self.responding:
            print("Changing current user")
            self.previoususer = msg['user']
            self.message += msg['text'] + " ;"
            self.responding = True
        if msg['user'] != self.previoususer and self.responding:
            print("Changing current user")
            self.previoususer = msg['user']
            self.response += msg['text'] + " ;"
            self.responding = False
            print("Storing Data in DB")
            message = self.message.replace("\'", "\'\'")
            response = self.response.replace("\'", "\'\'")
            cursor.execute(
                "INSERT INTO data(message, response) VALUES (\'{}\',\'{}\')".format(message.replace("  ", " "),
                                                                                    response.replace("  ", " ")))
            conn.commit()
            self.message = ""
            self.response = ""
        if msg['user'] == self.previoususer and not self.responding:
            self.message += msg['text'] + " "
        if msg['user'] == self.previoususer and self.responding:
            self.response += msg['text'] + " "

        cursor.execute("SELECT * FROM data;")
        res = cursor.fetchall()
        strings = []
        for i in range(0, len(res) - 1):
            count = 0
            for j in str(msg['text']).split():
                for k in str(res[i][0]).split():
                    if j == k:
                        self.matched = True
                        count += 1
                    elif not self.matched:
                        continue
                    else:
                        self.matched = False
                        break
            if count > len(str(msg['text']).split()) / 2 and count > len(str(res[i][0]).split()) / 2:
                strings.append(str(res[i][1]).replace(" ;", ""))
        if len(strings) > 0:
            self.post(msg['channel'], strings[randint(0, len(strings) - 1)])

    def getevent(self):
        msg = self.client.rtm_read()
        if msg:
            for action in msg:
                print(action)
                if ('type' in action) and (action['type'] == "message") and ("text" in action) and (
                        "bot_id" not in action):
                    self.process_message(action)
                elif ('type' in action) and (action['type'] == "reaction_added"):
                    self.react(action)


novabot = NovaBot()
while True:
    novabot.getevent()
