from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.app import App
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.uix.gridlayout import GridLayout
import boto3
from kivy.clock import Clock
import pymysql
from kivy.uix.image import AsyncImage
from kivy.uix.widget import Widget
import os
from kivymd.toast import toast
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivymd.uix.button import MDIconButton, MDRectangleFlatButton, MDFloatingActionButton , MDRoundFlatButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from screen_nav import screen_helper
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.core.window import Window
from kivy.graphics import Rectangle, Line, Color
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
Bucket_Name = "mobileappbucket-new"
s3_client = boto3.client('s3', aws_access_key_id="AKIA4WFGH2B7OWNMKKU4", aws_secret_access_key="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")
conn = pymysql.connect(host="localhost", user="root", password="Sharmi@2020", db="SnowRemovalApp")
cursor = conn.cursor()

screen_helper = """
#: import get_color_from_hex kivy.utils.get_color_from_hex
#:import NavigationLayout kivymd.uix.navigationdrawer.MDNavigationLayout
#:import Factory kivy.factory.Factory

ScreenManager:
    HomeScreen:
        name: 'home_screen'
    AdminLoginScreen:
        name: 'admin_login_screen'
    AdminHomeScreen:
        name: 'adminhome'
    AddLocationScreen:
        name: 'add_location_screen'
    ViewLocationScreen
        name: 'view_location_screen'
    AddCategoryScreen:
        name: 'add_category_screen'
    ViewCategoryScreen:
        name: 'view_category_screen'
    ViewProvidersScreen:
        name: 'view_providers_screen'
    ViewRequestScreen:
        name: 'view_request_screen'
    ViewHistoryScreen:
        name: 'view_history_screen'
    ViewPaymentsScreen:
        name: 'view_payments_screen'
    ViewCustomerComplaintsScreen:
        name: 'view_customer_complaint'
    ViewProviderComplaintsScreen:
        name: 'view_provider_complaint'


<AdminLoginScreen>
    admin_email : admin_email
    admin_password : admin_password
    BoxLayout:
        orientation: 'vertical'
        pos_hint: {"center_x":.5,"center_y":.8}
        padding: 40
        spacing: 20
        Widget:
            size_hint_y: 1
        MDLabel:
            text: "ADMIN LOGIN"
            color: 1, 1, 0.6, 1  # Pale yellow color in RGBA format
            font_name: "Comic"
            font_style: 'Button'
            font_size: 40
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 15
        MDTextField:
            id : admin_email
            hint_text: "Email"
            font_name: "Comic"
            icon_right: "account"
            mode: "round"
            size_hint_x: None
            width: 290
            font_size: 20
            pos_hint: {"center_x": .5}
            color_active: [1,1,1,1]
            normal_color : [1,1,0,1]
            on_text_validate: root.validate_provider_email(self)
        MDTextField:
            id : admin_password
            mode: "round"
            hint_text: "Password"
            font_name: "Comic"
            icon_right: "eye-off"
            size_hint_x: None
            width: 290
            font_size: 20
            pos_hint: {"center_x": .5}
            color_active: [1,1,1,1]
            password: True
            on_text: self.text = self.text.replace(" ", "")
        MDRoundFlatButton:
            text: "LOGIN"
            pos_hint: {"center_x": .5}
            font_size: 20
            md_bg_color: 0.2, 0.2, 0.2, 1  # Dark grey background color
            text_color: 1, 1, 1, 1  # White text color
            on_press: root.admin_login()

<AdminHomeScreen>
    MDTopAppBar:
        title: "Snow Removal"
        pos_hint: {"top": 1}
        elevation: 10
    GridLayout:
        cols: 2
        spacing: 20
        padding: 10
        size_hint_y: None
        height: self.minimum_height
        pos_hint: {"center_x": 0.7, "center_y": 0.5}
        MDCard:
            orientation: 'vertical'
            size_hint: None, None
            size: "100dp", "100dp"
            md_bg_color: 0, 0.5, 0.5, 1  # Teal color (RGBA)
            on_press: root.on_card_press('view_providers_screen')
            MDLabel:
                text: "View Providers"
                font_size: 20
                font_name: "Comic"
                halign: "center"
        MDCard:
            orientation: 'vertical'
            size_hint: None, None
            size: "100dp", "100dp"
            md_bg_color: 0, 0.5, 0.5, 1  # Teal color (RGBA)
            on_press: root.on_card_press('add_location_screen')
            MDLabel:
                text: "Add Locations"
                font_size: 20
                font_name: "Comic"
                halign: "center"
        MDCard:
            orientation: 'vertical'
            size_hint: None, None
            size: "100dp", "100dp"
            md_bg_color: 0, 0.5, 0.5, 1  # Teal color (RGBA)
            on_press: root.on_card_press('view_location_screen')
            MDLabel:
                text: "View Locations"
                font_size: 20
                font_name: "Comic"
                halign: "center"
        MDCard:
            orientation: 'vertical'
            size_hint: None, None
            size: "100dp", "100dp"
            md_bg_color: 0, 0.5, 0.5, 1  # Teal color (RGBA)
            on_press: root.on_card_press('add_category_screen')
            MDLabel:
                text: "Add Category"
                font_size: 20
                font_name: "Comic"
                halign: "center"
        MDCard:
            orientation: 'vertical'
            size_hint: None, None
            size: "100dp", "100dp"
            md_bg_color: 0, 0.5, 0.5, 1  # Teal color (RGBA)
            on_press: root.on_card_press('view_category_screen')
            MDLabel:
                text: "View Category"
                font_size: 20
                font_name: "Comic"
                halign: "center"
        MDCard:
            orientation: 'vertical'
            size_hint: None, None
            size: "100dp", "100dp"
            md_bg_color: 0, 0.5, 0.5, 1  # Teal color (RGBA)
            on_press: root.on_card_press('view_request_screen')
            MDLabel:
                text: "View Requests"
                font_size: 20
                font_name: "Comic"
                halign: "center"
        MDCard:
            orientation: 'vertical'
            size_hint: None, None
            size: "100dp", "100dp"
            md_bg_color: 0, 0.5, 0.5, 1  # Teal color (RGBA)
            on_press: root.on_card_press('view_history_screen')
            MDLabel:
                text: "View History"
                font_size: 20
                font_name: "Comic"
                halign: "center"
    BoxLayout:
        orientation: 'vertical'
        size_hint: None, None
        size: "200dp", "50dp"
        pos_hint: {"center_x": 0.5, "center_y": 0.1}
        MDRaisedButton:
            text: "Logout"
            size_hint: None, None
            size: 200, 50
            pos_hint: {"center_x": 0.5}
            on_release: root.manager.current = 'admin_login_screen'

<AddLocationScreen>
    location_name : location_name
    zip_code: zip_code
    MDCard:
        size_hint: None,None
        size: 450,600
        pos_hint: {"center_x":.5,"center_y":.5}
        elevation: 5
        md_bg_color: [0, 0, 0, 1]  # Black color (RGBA)
        padding: 9
        spacing: 
        orientation: "vertical"
        MDLabel:
            text: "Add Location"
            font_size: 30
            font_name: "Comic"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            color: 1, 0.647, 0, 1  # Orange color (RGBA)
        Widget:
            size_hint_y: None
            height: 40
        Spinner:
            id: state_spinner
            pos_hint: {"center_x": .5}
            font_name: "Comic"
            text: 'Select Sate'
            md_bg_color: 0.2, 0.2, 0.2, 1  # Dark grey background color
            text_color: 1, 1, 1, 1  # White text color
            values: ["New Hampshire", "Maine", "Vermont", "Alaska", "Wyoming", "Michigan", "New York", "Utah", "Minnesota", "Massachusetts"]
            on_text: root.update_city_spinner(self.text)
        Widget:
            size_hint_y: None
            height: 10
        Spinner:
            id: city_spinner
            pos_hint: {"center_x": .5}
            font_name: "Comic"
            text: 'Select City'
            md_bg_color: 0.2, 0.2, 0.2, 1  # Dark grey background color
            text_color: 1, 1, 1, 1  # White text color
        Widget:
            size_hint_y: None
            height: 20
        MDTextField:
            id : location_name
            hint_text: "Location Name"
            font_name: "Comic"
            size_hint_x: None
            width: 290
            font_size: 20
            pos_hint: {"center_x": .5}
            color_active: 1, 0.647, 0, 1  # Orange (RGBA)
            normal_color: 1, 1, 1, 1  # White (RGBA)
        MDTextField:
            id : zip_code
            hint_text: "Zip Code"
            font_name: "Comic"
            size_hint_x: None
            width: 290
            font_size: 20
            pos_hint: {"center_x": .5}
            color_active: 1, 0.647, 0, 1  # Orange (RGBA)
            normal_color: 1, 1, 1, 1  # White (RGBA)
        MDRoundFlatButton:
            id: location_picture
            text: "Select Location Picture"
            pos_hint: {"center_x": .5}
            font_size: 20
            text_color: 1, 1, 1, 1  # RGBA values for white
            md_bg_color: 0, 0.502, 0.502, 1  # Teal color in RGBA format
            on_press : root.location_button()
        Widget:
            size_hint_y: None
            height: 10
        Image:
            id : location_picture
            size_hint: None, None  # Set the size hint to 50% of the card's size
            size: dp(100), dp(100)
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            allow_stretch: True
            keep_ratio: True
            height: 100  # Set a height for the image widget
            opacity: 0 
        MDRoundFlatButton:
            text: "ADD LOCATION"
            pos_hint: {"center_x": .5}
            font_size: 20
            on_press: root.add_location_data()
    MDIconButton:
        icon: 'arrow-left'
        pos_hint: {"center_x": .5}
        font_size: 20
        on_press: root.manager.current='adminhome'

<ViewLocationScreen>
    BoxLayout:
        orientation: 'vertical'
        padding: 20  # Add padding to create a gap around the contents
        ScrollView:
            GridLayout:
                id: location_table_layout
                cols: 1  # Set to 1 since we want one card per row
                spacing: 20  # Add spacing between the cards
                size_hint_y: None
                height: self.minimum_height  # Add this line
        MDIconButton:
            icon: 'arrow-left'
            pos_hint: {"center_x": .5}
            font_size: 20
            on_press: root.manager.current='adminhome'

<AddCategoryScreen>
    category_name : category_name
    MDCard:
        size_hint: None,None
        size: 450,500
        pos_hint: {"center_x":.5,"center_y":.5}
        elevation: 5
        md_bg_color: [0, 0, 0, 1]  # Black color (RGBA)
        padding: 9
        spacing: 
        orientation: "vertical"
        MDLabel:
            text: "Add Category"
            font_size: 30
            font_name: "Comic"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            color: 1, 0.647, 0, 1  # Orange color (RGBA)
        Widget:
            size_hint_y: None
            height: 40
        MDTextField:
            id : category_name
            hint_text: "Category Name"
            font_name: "Comic"
            size_hint_x: None
            width: 290
            font_size: 20
            pos_hint: {"center_x": .5}
            color_active: 1, 0.647, 0, 1  # Orange (RGBA)
            normal_color: 1, 1, 1, 1  # White (RGBA)
        MDRoundFlatButton:
            id: category_picture
            text: "Select Category Picture"
            pos_hint: {"center_x": .5}
            font_size: 20
            text_color: 1, 1, 1, 1  # RGBA values for white
            md_bg_color: 0, 0.502, 0.502, 1  # Teal color in RGBA format
            on_press : root.category_button()
        Widget:
            size_hint_y: None
            height: 10
        Image:
            id : category_image
            size_hint: None, None  # Set the size hint to 50% of the card's size
            size: dp(100), dp(100)
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            allow_stretch: True
            keep_ratio: True
            height: 100  # Set a height for the image widget
            opacity: 0 
        MDRoundFlatButton:
            text: "ADD CATEGORY"
            pos_hint: {"center_x": .5}
            font_size: 20
            on_press: root.add_category_data()
    MDIconButton:
        icon: 'arrow-left'
        pos_hint: {"center_x": .5}
        font_size: 20
        on_press: root.manager.current='adminhome'

<ViewCategoryScreen>
    BoxLayout:
        orientation: 'vertical'
        padding: 20  # Add padding to create a gap around the contents
        ScrollView:
            GridLayout:
                id: category_table_layout
                cols: 1  # Set to 1 since we want one card per row
                spacing: 20  # Add spacing between the cards
                size_hint_y: None
                height: self.minimum_height  # Add this line
        MDIconButton:
            icon: 'arrow-left'
            pos_hint: {"center_x": .5}
            font_size: 20
            on_press: root.manager.current='adminhome'

<ViewProvidersScreen>
    BoxLayout:
        orientation: 'vertical'
        padding: 20  # Add padding to create a gap around the contents
        ScrollView:
            GridLayout:
                id: admin_view_provider_cards_layout
                cols: 1
                spacing: 0
                size_hint_y: None
                height: self.minimum_height
                padding: 5  # Add this line
                spacing: 10  # Add this line
    MDIconButton:
        icon: 'arrow-left'
        pos_hint: {"center_x": .5}
        font_size: 20
        on_press: root.manager.current='adminhome'

<ViewRequestScreen>
    BoxLayout:
        orientation: 'vertical'
        pos_hint: {'center_x': 0.4}
        padding: 50  # Add padding to create a gap around the contents
        spacing: 10
        ScrollView:
            GridLayout:
                id: admin_service_cards_layout
                cols: 1  # Set to 1 since we want one card per row
                size_hint_y: None
                height: self.minimum_height
                padding: 5  # Add this line
                spacing: 10  # Add this line
    MDIconButton:
        icon: 'arrow-left'
        pos_hint: {"center_x": .5}
        font_size: 20
        on_press: root.manager.current='adminhome'

<ViewHistoryScreen>
    BoxLayout:
        orientation: 'vertical'
        pos_hint: {'center_x': 0.4}
        padding: 50  # Add padding to create a gap around the contents
        spacing: 10
        ScrollView:
            GridLayout:
                id: admin_view_history_layout
                cols: 1  # Set to 1 since we want one card per row
                size_hint_y: None
                height: self.minimum_height
                padding: 5  # Add this line
                spacing: 10  # Add this line
    MDIconButton:
        icon: 'arrow-left'
        pos_hint: {"center_x": .5}
        font_size: 20
        on_press: root.manager.current='adminhome'

<ViewPaymentsScreen>
    BoxLayout:
        orientation: 'vertical'
        padding: 50  # Add padding to create a gap around the contents
        ScrollView:
            GridLayout:
                id: view_payment_layout
                cols: 4  # Set to 1 since we want one card per row
                spacing: 20  # Add spacing between the cards
    MDIconButton:
        icon: 'arrow-left'
        pos_hint: {"center_x": .5}
        font_size: 20
        on_press: root.manager.current='adminhome'

<ViewCustomerComplaintsScreen>
    BoxLayout:
        orientation: 'vertical'
        padding: 50  # Add padding to create a gap around the contents
        ScrollView:
            GridLayout:
                id: view_complaints_screen
                cols: 2  # Set to 1 since we want one card per row
                spacing: 20  # Add spacing between the cards
    MDIconButton:
        icon: 'arrow-left'
        pos_hint: {"center_x": .5}
        font_size: 20
        on_press: root.manager.current='adminhome'

<ViewProviderComplaintsScreen>
    BoxLayout:
        orientation: 'vertical'
        padding: 50  # Add padding to create a gap around the contents
        ScrollView:
            GridLayout:
                id: view_provider_complaints_screen
                cols: 2  # Set to 1 since we want one card per row
                spacing: 20  # Add spacing between the cards
    MDIconButton:
        icon: 'arrow-left'
        pos_hint: {"center_x": .5}
        font_size: 20
        on_press: root.manager.current='adminhome'
"""

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        home_icon = MDFloatingActionButton(
            icon="static/myfiles/1.png",
            size=(100, 100),  # Set the size as needed
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            on_release=self.go_to_dashboard  # Set the on_release event
        )

        label = MDLabel(
            text="Snow Removal App",
            halign="center",
            font_style="H5",
            pos_hint={'center_x': 0.5, 'center_y': 0.45},
            theme_text_color="Primary",
        )

        self.add_widget(home_icon)
        self.add_widget(label)

    def go_to_dashboard(self, instance):
        self.manager.current = 'admin_login_screen'

class AdminLoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def admin_login(self):
        admin_email = self.admin_email.text
        admin_password = self.admin_password.text
        if admin_email == 'admin@gmail.com' and admin_password == 'admin':
            self.manager.current = 'adminhome'
            toast("Login Successfull")
        else:
            toast("Invalid Login Details")

        self.admin_email.text = ''
        self.admin_password.text = ''

class AdminHomeScreen(Screen):

    def on_card_press(self, screen_name):
        if screen_name == 'add_location_screen':
            self.manager.current = 'add_location_screen'
        elif screen_name == 'view_location_screen':
            self.manager.current = 'view_location_screen'
        elif screen_name == 'add_category_screen':
            self.manager.current = 'add_category_screen'
        elif screen_name == 'view_category_screen':
            self.manager.current = 'view_category_screen'
        elif screen_name == 'view_request_screen':
            self.manager.current = 'view_request_screen'
        elif screen_name == 'view_history_screen':
            self.manager.current = 'view_history_screen'
        elif screen_name == 'view_providers_screen':
            self.manager.current = 'view_providers_screen'
        elif screen_name == 'view_request_screen':
            self.manager.current = 'view_request_screen'
        elif screen_name == 'view_history_screen':
            self.manager.current = 'view_history_screen'

class AddLocationScreen(Screen):

    location_name = ObjectProperty(None)
    zip_code = ObjectProperty(None)

    def update_city_spinner(self, selected_state):
        state_city_mapping = {
            "New Hampshire": ["Pittsburg"],
            "Maine": ["Stratton"],
            "Vermont": ["Cabot"],
            "Alaska": ["Juneau"],
            "Wyoming": ["Moose"],
            "Michigan": ["Houghton"],
            "New York": ["Ava", "Buffalo", "Rochester", "Syracuse"],
            "Utah": ["Alta", "Heber", "Cedar City", "Millcreek"],
            "Minnesota": ["Duluth"],
            "Massachusetts": ["Fitchburg", "Worcester", "Pittsfield"]
            # Add mappings for other states
        }

        # Update the values of the city_spinner based on the selected state
        city_spinner = self.ids.city_spinner
        city_spinner.values = state_city_mapping.get(selected_state, [])

        city_spinner.text = 'Select City'

    def add_location_data(self):
        location_name = self.location_name.text
        zip_code = self.zip_code.text
        selected_state = self.ids.state_spinner.text
        selected_city = self.ids.city_spinner.text
        location_picture = self.ids.location_picture.source

        if not (location_name and location_picture and selected_state and selected_city and zip_code):
            toast("All fields are required")
            return

        location_file_name = os.path.basename(location_picture)
        s3_client.upload_file(location_picture, Bucket_Name, location_file_name)
        bucket_name = 'mobileappbucket-new'
        s3_file_name = location_file_name

        location_image_url = f'https://{bucket_name}.s3.amazonaws.com/{s3_file_name}'
        count = cursor.execute("select * from location where location_name = '" + str(location_name) + "'")
        if count == 0:
            query = ("insert into location(location_name,city,state,zipcode,location_picture) values('" + str(location_name) + "' , '" + str(selected_city) + "' , '" + str(selected_state) + "' , '"+str(zip_code)+"'  ,'" + str(location_image_url) + "')")
            cursor.execute(query)
            conn.commit()
            toast("Location Added Successfull")
        else:
            toast("Duplicate Details")

        self.location_name.text = ''
        self.zip_code.text = ''
        self.ids.state_spinner.text = ''
        self.ids.location_picture.source = ''
        self.ids.city_spinner.text = ''

    def location_button(self):
        from plyer import filechooser
        filechooser.open_file(on_selection=self.selected)

    def selected(self, selection):
        self.ids.location_picture.source = selection[0]
        self.ids.location_picture.opacity = 1
        toast("Location Picture Selected")

class ViewLocationScreen(Screen):

    def __init__(self, **kwargs):
        super(ViewLocationScreen, self).__init__(**kwargs)

    def on_pre_enter(self, *args):
        # This method is called just before the screen is displayed.
        # You can add code here to update the displayed locations.
        self.update_location_list()

    def update_location_list(self):
        light_color = [0.5, 0.5, 0.5, 1]  # RGB values for a light gray color
        try:
            location_table_layout = self.ids['location_table_layout']
            location_table_layout.padding = [60]  # Add padding around the GridLayout
            location_table_layout.spacing = 20  # Add spacing between the cards
            location_table_layout.clear_widgets()

            cursor.execute("SELECT location_name,city,state,location_picture,zipcode FROM location")
            locations = cursor.fetchall()
            if locations:
                for location in locations:
                    location_name = location[0]
                    city = location[1]
                    state = location[2]
                    location_picture = location[3]
                    zipcode = location[4]

                    location_name_label = MDLabel(text=str(location_name))
                    city_label = MDLabel(text=city)
                    state_label = MDLabel(text=state)
                    zipcode_label = MDLabel(text=zipcode)
                    location_picture_label = AsyncImage(source=location_picture, keep_ratio=True, allow_stretch=True)

                    card = MDCard(
                        orientation='vertical',
                        size_hint=(None, None),
                        size=(400, 400),
                        elevation=5,  # Add elevation for shadow effect
                        padding=10
                    )

                    box1 = MDBoxLayout(orientation='vertical')  # Add spacing between labels

                    state_text = MDLabel(
                        text="State:",
                        theme_text_color="Custom",
                        text_color=light_color,
                        font_style="Caption",
                        size_hint_y=None,
                    )
                    box1.add_widget(state_text)
                    box1.add_widget(state_label)

                    city_text = MDLabel(
                        text="City:",
                        theme_text_color="Custom",
                        text_color=light_color,
                        font_style="Caption",
                        size_hint_y=None,
                    )
                    box1.add_widget(city_text)
                    box1.add_widget(city_label)

                    location_name = MDLabel(
                        text="Location Name:",
                        theme_text_color="Custom",
                        text_color=light_color,
                        font_style="Caption",
                        size_hint_y=None,
                    )
                    box1.add_widget(location_name)
                    box1.add_widget(location_name_label)

                    zip_code = MDLabel(
                        text="Zip Code:",
                        theme_text_color="Custom",
                        text_color=light_color,
                        font_style="Caption",
                        size_hint_y=None,
                    )
                    box1.add_widget(zip_code)
                    box1.add_widget(zipcode_label)

                    box2 = MDBoxLayout(orientation='vertical')
                    box2.add_widget(location_picture_label)

                    box = MDBoxLayout(orientation='horizontal')
                    box.add_widget(box1)
                    box.add_widget(box2)

                    # Add the box layout to the card
                    card.add_widget(box)

                    location_table_layout.add_widget(card)
            else:
                # Handle case where no locations are found
                no_location_label = MDLabel(text="No Locations Found", font_size=30, theme_text_color="Custom",halign="center",text_color=(1, 1, 1, 1))
                self.ids['location_table_layout'].add_widget(no_location_label)

        except Exception as e:
            print(f"An error occurred: {e}")

class AddCategoryScreen(Screen):

    category_name = ObjectProperty(None)

    def add_category_data(self):
        category_name = self.category_name.text
        category_picture = self.ids.category_image.source

        if not (category_name and category_picture):
            toast("All fields are required")
            return

        category_file_name = os.path.basename(category_picture)
        s3_client.upload_file(category_picture, Bucket_Name, category_file_name)
        bucket_name = 'mobileappbucket-new'
        s3_file_name = category_file_name

        category_image_url = f'https://{bucket_name}.s3.amazonaws.com/{s3_file_name}'
        count = cursor.execute("select * from category where category_name = '" + str(category_name) + "'")
        if count == 0:
            query = ("insert into category(category_name,category_picture) values('" + str(category_name) + "' , '" + str(category_image_url) + "')")
            cursor.execute(query)
            conn.commit()
            toast("Category Added Successfull")
        else:
            toast("Duplicate Details")

        self.category_name.text = ''
        self.ids.category_picture.source = ''

    def category_button(self):
        from plyer import filechooser
        filechooser.open_file(on_selection=self.category_selected)

    def category_selected(self, selection):
        self.ids.category_image.source = selection[0]
        self.ids.category_image.opacity = 1
        toast("Category Image Selected")

class ViewCategoryScreen(Screen):

    def __init__(self, **kwargs):
        super(ViewCategoryScreen, self).__init__(**kwargs)

    def on_pre_enter(self, *args):
        # This method is called just before the screen is displayed.
        # You can add code here to update the displayed locations.
        self.update_category_list()

    def update_category_list(self):
        light_color = [0.5, 0.5, 0.5, 1]  # RGB values for a light gray color

        category_table_layout = self.ids['category_table_layout']
        category_table_layout.padding = [60]  # Add padding around the GridLayout
        category_table_layout.spacing = 20  # Add spacing between the cards
        category_table_layout.clear_widgets()

        cursor.execute("SELECT category_name,category_picture FROM category")
        categories = cursor.fetchall()
        if categories:
            for category in categories:
                category_name = category[0]
                category_picture = category[1]

                category_name_label = MDLabel(text=category_name)
                category_picture_label = AsyncImage(source=category_picture)

                card = MDCard(
                    orientation='vertical',
                    size_hint=(None, None),
                    size=(400, 350),
                    elevation=5,  # Add elevation for shadow effect
                    padding=10
                )

                Category_Name = MDLabel(
                    text="Category Name:",
                    theme_text_color="Custom",
                    text_color=light_color,
                    font_style="Caption",
                )
                card.add_widget(Category_Name)
                card.add_widget(category_name_label)

                Category_Image = MDLabel(
                    text="Category Image:",
                    theme_text_color="Custom",
                    text_color=light_color,
                    font_style="Caption",
                )
                card.add_widget(Category_Image)
                card.add_widget(category_picture_label)

                category_table_layout.add_widget(card)
        else:
            no_category_label = MDLabel(
                text="No Categories Found",
                font_size=30,
                theme_text_color="Custom",
                halign="center",
                text_color=(1, 1, 1, 1)
            )
            category_table_layout.add_widget(no_category_label)

class ViewProvidersScreen(Screen):

    def __init__(self, **kwargs):
        super(ViewProvidersScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.view_providers_populate_table)

    def view_providers_populate_table(self, *args):
        admin_view_provider_cards_layout = self.ids['admin_view_provider_cards_layout']
        admin_view_provider_cards_layout.clear_widgets()  # Clear existing widgets
        admin_view_provider_cards_layout.padding = [40]  # Add padding around the GridLayout
        admin_view_provider_cards_layout.spacing = 20  # Add spacing between the cards

        cursor.execute("SELECT * FROM service_provider")
        service_providers = cursor.fetchall()

        if not service_providers:
            # Display a label if there are no service providers
            no_providers_label = MDLabel(
                text="No service providers found",
                font_size=20,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),  # White text color
                halign="center"
            )
            no_providers_label.font_size = 22
            admin_view_provider_cards_layout.add_widget(no_providers_label)
            return

        for service_provider in service_providers:
            service_provider_id = service_provider[0]
            name = service_provider[1]
            email = service_provider[2]
            phone = service_provider[3]
            password = service_provider[4]
            address = service_provider[5]
            profile_picture = service_provider[6]
            license = service_provider[7]
            id_proof = service_provider[8]
            status = service_provider[9]

            card = MDCard(
                orientation='vertical',
                size_hint=(None, None),
                size=(600, 450),
                elevation=5,
                padding=15,
                spacing=10,
                md_bg_color=(0.9, 0.9, 0.9, 1)
            )

            image_layout = MDBoxLayout(orientation='horizontal', spacing=10)
            profile_picture = AsyncImage(source=profile_picture)
            license_image = AsyncImage(source=license)
            id_proof_image = AsyncImage(source=id_proof)
            image_layout.add_widget(profile_picture)
            image_layout.add_widget(license_image)
            image_layout.add_widget(id_proof_image)

            # Second part: Textual information
            text_layout = GridLayout(cols=2, spacing=10)

            black_text_style = {"theme_text_color": "Custom", "text_color": (0, 0, 0, 1)}

            text_layout.add_widget(MDLabel(text="Name:", **black_text_style))
            text_layout.add_widget(MDLabel(text=name, **black_text_style))
            text_layout.add_widget(MDLabel(text="Email:", **black_text_style))
            text_layout.add_widget(MDLabel(text=email, **black_text_style))
            text_layout.add_widget(MDLabel(text="Phone:", **black_text_style))
            text_layout.add_widget(MDLabel(text=phone, **black_text_style))
            text_layout.add_widget(MDLabel(text="Password:", **black_text_style))
            text_layout.add_widget(MDLabel(text=password, **black_text_style))
            text_layout.add_widget(MDLabel(text="Address:", **black_text_style))
            text_layout.add_widget(MDLabel(text=address, **black_text_style))
            text_layout.add_widget(MDLabel(text="Status:", **black_text_style))
            text_layout.add_widget(MDLabel(text=status, **black_text_style))

            buttons_layout = MDBoxLayout(spacing=10)
            initial_status_text = 'Deactivate' if status == 'Activate' else 'Activate'
            button = MDRectangleFlatButton(
                text=initial_status_text,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),  # White color
                md_bg_color=(0, 0.5, 0.5, 1),  # Teal color
            )
            button.service_provider_id = service_provider_id
            button.bind(on_press=self.handle_status_change)
            buttons_layout.add_widget(button)

            card.orientation = 'vertical'
            card.add_widget(image_layout)
            card.add_widget(text_layout)
            card.add_widget(buttons_layout)

            admin_view_provider_cards_layout.add_widget(card)

    def handle_status_change(self, instance):
        # Get the corresponding service provider ID
        service_provider_id = instance.service_provider_id

        # Retrieve the current status from the database
        cursor.execute("SELECT status FROM service_provider WHERE service_provider_id = %s", (service_provider_id,))
        current_status = cursor.fetchone()[0]

        # Update the status in the database
        new_status = 'Deactivate' if current_status == 'Activate' else 'Activate'
        cursor.execute("UPDATE service_provider SET status = %s WHERE service_provider_id = %s",(new_status, service_provider_id)
        )
        conn.commit()

        # Update the button text
        instance.text = 'Activate' if new_status == 'Deactivate' else 'Deactivate'

        # Refresh the UI
        self.view_providers_populate_table()

class ViewRequestScreen(Screen):
    def __init__(self, **kwargs):
        super(ViewRequestScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.viewrequest_populate_table)
        Clock.schedule_interval(self.check_for_updates, 60)

    def check_for_updates(self, dt):
        # Query the database for updates and update the UI accordingly
        self.viewrequest_populate_table()

    def viewrequest_populate_table(self, *args):
        try:
            admin_service_cards_layout = self.ids['admin_service_cards_layout']
            admin_service_cards_layout.clear_widgets()  # Clear existing widgets
            admin_service_cards_layout.padding = [40]  # Add padding around the GridLayout
            admin_service_cards_layout.spacing = 20  # Add spacing between the cards

            cursor.execute("select * from service")
            services = cursor.fetchall()
            service_ids = [service[0] for service in services]
            if service_ids:  # Check if service_ids list is not empty
                cursor.execute("SELECT * FROM service_booking WHERE service_id IN %s AND (status = 'Request Sended' OR status = 'Accepted Request' OR status = 'Paid Advance Amount' OR status = 'Service Completed')",(tuple(service_ids),))
                service_provider_view_requests = cursor.fetchall()

                if not service_provider_view_requests:
                    no_requests_label = MDLabel(
                        text="No Requests Found",
                        font_size=30,
                        text_color=(1, 1, 1, 1),
                        theme_text_color="Custom",
                        halign="center"
                    )
                    no_requests_label.font_size = 30
                    admin_service_cards_layout.add_widget(no_requests_label)
                    return

                for service_booking in service_provider_view_requests:
                    service_booking_id = service_booking[0]
                    service_id = service_booking[8]
                    number_of_sq_feet = float(service_booking[1])
                    description = service_booking[2]
                    status = service_booking[7]
                    customer_id = service_booking[9]
                    booking_date = service_booking[3]

                    cursor.execute("SELECT status FROM service_booking WHERE service_booking_id = '"+str(service_booking_id)+"'")
                    new_status_result = cursor.fetchone()

                    if new_status_result:
                        new_status = new_status_result[0]
                    else:
                        new_status = status

                    if new_status != status:
                        status = new_status

                    if status in ["Rejected Request", "Request Cancelled by Customer"]:
                        continue  # Skip this card

                    cursor.execute("select * from service where service_id = '" + str(service_id) + "'")
                    service = cursor.fetchone()
                    service_image = service[4]
                    charger_per_sq_feet = float(service[3])

                    total_charge = number_of_sq_feet * charger_per_sq_feet
                    advance_payment = total_charge * 0.2
                    remaining_amount = total_charge - advance_payment

                    service_name_provider = ViewRequestScreen.get_service_name_from_ProviderViewRequests(service_id)
                    customer_data = ViewRequestScreen.get_customer_name_from_service(customer_id)

                    service_provider_details_customer = ViewRequestScreen.get_service_provider_details_from_service(service_id)
                    service_provider_name, service_provider_email, service_provider_phone = service_provider_details_customer

                    card = MDCard(
                        orientation='vertical',
                        size_hint=(None, None),
                        size=(550, 870),
                        elevation=5,
                        padding=15,
                        md_bg_color=(0.9, 0.9, 0.9, 1)
                    )

                    number_of_sq_feet_provider = MDLabel(text=str(number_of_sq_feet), font_size=15,
                                                         text_color=(0, 0, 0.5, 1), theme_text_color="Custom")
                    description_provider = MDLabel(text=str(description), font_size=15, text_color=(0, 0, 0.5, 1),
                                                   theme_text_color="Custom")
                    booking_date_provider = MDLabel(text=str(booking_date), font_size=15, text_color=(0, 0, 0.5, 1),
                                                    theme_text_color="Custom")
                    status_provider = MDLabel(
                        text=str(status),
                        theme_text_color="Custom",
                        text_color=(0.5, 0, 0.5, 1),  # RGB values for purple
                        bold=True,
                        font_size=15,
                    )
                    service_name_provider_label = MDLabel(text=service_name_provider, font_size=15,
                                                          text_color=(0, 0, 0.5, 1), theme_text_color="Custom")
                    charger_per_sq_feet_provider = MDLabel(text=f"${charger_per_sq_feet}", font_size=15,
                                                           text_color=(0, 0, 0.5, 1), theme_text_color="Custom")
                    service_picture_provider = AsyncImage(source=service_image, keep_ratio=True, allow_stretch=True)

                    box1 = MDBoxLayout(orientation='vertical')  # Add spacing between labels

                    service_name_data_provider = MDLabel(
                        text="Service Name:",
                        theme_text_color="Custom",
                        font_style="Caption",
                        size_hint_y=None,
                        height=20
                    )
                    box1.add_widget(service_name_data_provider)
                    box1.add_widget(Widget(size_hint_y=None, height=10))  # Adjust the height value as needed
                    box1.add_widget(service_name_provider_label)

                    spacer = Widget(size_hint_y=None, height=30)
                    box1.add_widget(spacer)

                    charge_per_sq_feet_data_provider = MDLabel(
                        text="Charger Per sq.feet:",
                        theme_text_color="Custom",
                        font_style="Caption",
                        size_hint_y=None,
                        height=20
                    )
                    box1.add_widget(charge_per_sq_feet_data_provider)
                    box1.add_widget(Widget(size_hint_y=None, height=10))  # Adjust the height value as needed
                    box1.add_widget(charger_per_sq_feet_provider)

                    spacer = Widget(size_hint_y=None, height=30)
                    box1.add_widget(spacer)

                    number_of_sq_feet_data_provider = MDLabel(
                        text="No.of sq.feet:",
                        theme_text_color="Custom",
                        font_style="Caption",
                        size_hint_y=None,
                        height=20
                    )
                    box1.add_widget(number_of_sq_feet_data_provider)
                    box1.add_widget(Widget(size_hint_y=None, height=10))  # Adjust the height value as needed
                    box1.add_widget(number_of_sq_feet_provider)

                    spacer = Widget(size_hint_y=None, height=30)
                    box1.add_widget(spacer)

                    description_data_provider = MDLabel(
                        text="Description:",
                        theme_text_color="Custom",
                        font_style="Caption",
                        size_hint_y=None,
                        height=20
                    )
                    box1.add_widget(description_data_provider)
                    box1.add_widget(Widget(size_hint_y=None, height=10))  # Adjust the height value as needed
                    box1.add_widget(description_provider)

                    spacer = Widget(size_hint_y=None, height=30)
                    box1.add_widget(spacer)

                    booking_provider = MDLabel(
                        text="Booking Date:",
                        theme_text_color="Custom",
                        font_style="Caption",
                        size_hint_y=None,
                        height=20
                    )
                    box1.add_widget(booking_provider)
                    box1.add_widget(Widget(size_hint_y=None, height=10))  # Adjust the height value as needed
                    box1.add_widget(booking_date_provider)

                    spacer = Widget(size_hint_y=None, height=30)
                    box1.add_widget(spacer)

                    if service_booking[7] in ["Request Sended", "Paid Advance Amount", "Rejected Request", "Cancelled by customer", "Accepted Request", "Service Completed", "Full Payment Successfull"]:
                        status_data_provider = MDLabel(
                            text="Status:",
                            theme_text_color="Custom",
                            font_style="Caption",
                            size_hint_y=None,
                            height=20
                        )
                        box1.add_widget(status_data_provider)
                        box1.add_widget(Widget(size_hint_y=None, height=10))  # Adjust the height value as needed
                        box1.add_widget(status_provider)

                    spacer = Widget(size_hint_y=None, height=30)
                    box1.add_widget(spacer)

                    Customer_Details = MDLabel(
                        text="Customer Details",
                        theme_text_color="Custom",
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30)
                    )
                    box1.add_widget(Customer_Details)
                    box1.add_widget(Widget(size_hint_y=None, height=10))  # Adjust the height value as needed
                    if customer_data is not None:
                        customer_name = customer_data[0]  # Access the customer name
                        phone_number = customer_data[1]  # Access the phone number
                        address = customer_data[2]
                        customer_name_data_label = MDLabel(
                            text=f"Name: {customer_name}",
                            font_size=13,
                            text_color=(0, 0, 0.5, 1),
                            theme_text_color="Custom"
                        )
                        box1.add_widget(customer_name_data_label)

                        box1.add_widget(Widget(size_hint_y=None, height=25))  # Adjust the height value as needed

                        customer_phone_data_label = MDLabel(
                            text=f"Phone: {phone_number}",
                            font_size=13,
                            text_color=(0, 0, 0.5, 1),
                            theme_text_color="Custom"
                        )
                        box1.add_widget(customer_phone_data_label)

                        box1.add_widget(Widget(size_hint_y=None, height=25))  # Adjust the height value as needed

                        customer_address_label = MDLabel(
                            text=f"Address: {address}",
                            font_size=13,
                            text_color=(0, 0, 0.5, 1),
                            theme_text_color="Custom"
                        )
                        box1.add_widget(customer_address_label)
                    else:
                        print("No matching customer found.")

                    spacer = Widget(size_hint_y=None, height=35)
                    box1.add_widget(spacer)

                    Provider_Details = MDLabel(
                        text="Provider Details",
                        theme_text_color="Custom",
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30)
                    )
                    box1.add_widget(Provider_Details)

                    box1.add_widget(Widget(size_hint_y=None, height=25))  # Adjust the height value as needed

                    if service_provider_details_customer is not None:
                        name = service_provider_name  # Access the customer name
                        phone_number = service_provider_phone  # Access the phone number
                        email = service_provider_email
                        provider_name_data_label = MDLabel(
                            text=f"Name: {name}",
                            font_size=13,
                            height=20,
                            text_color=(0, 0, 0.5, 1),
                            theme_text_color="Custom"
                        )
                        box1.add_widget(provider_name_data_label)

                        box1.add_widget(Widget(size_hint_y=None, height=25))  # Adjust the height value as needed

                        provider_phone_data_label = MDLabel(
                            text=f"Phone: {phone_number}",
                            font_size=13,
                            height=20,
                            text_color=(0, 0, 0.5, 1),
                            theme_text_color="Custom"
                        )
                        box1.add_widget(provider_phone_data_label)

                        box1.add_widget(Widget(size_hint_y=None, height=25))  # Adjust the height value as needed

                        provider_address_label = MDLabel(
                            text=f"Email: {email}",
                            font_size=13,
                            height=20,
                            text_color=(0, 0, 0.5, 1),
                            theme_text_color="Custom"
                        )
                        box1.add_widget(provider_address_label)
                    else:
                        print("No matching provider found.")

                    spacer = Widget(size_hint_y=None, height=35)
                    box1.add_widget(spacer)

                    if service_booking[7] in ["Request Sended", "Accepted Request"]:
                        total_charge = MDLabel(
                            text=f"Total Charge: ${total_charge}",
                            theme_text_color="Custom",
                            text_color=(0.5, 0, 0.5, 1),
                            font_style="Caption",
                            size_hint_y=None,
                            height=dp(30),
                            bold=True
                        )
                        box1.add_widget(total_charge)

                        advance_amount = MDLabel(
                            text=f"Advance Amount: ${advance_payment}",
                            theme_text_color="Custom",
                            text_color=(0.5, 0, 0.5, 1),
                            font_style="Caption",
                            size_hint_y=None,
                            height=dp(30),
                            bold=True
                        )
                        box1.add_widget(advance_amount)

                        remaining_amount = MDLabel(
                            text=f"Remaining Amount: ${remaining_amount}",
                            theme_text_color="Custom",
                            text_color=(0.5, 0, 0.5, 1),
                            font_style="Caption",
                            size_hint_y=None,
                            height=dp(30),
                            bold=True
                        )
                        box1.add_widget(remaining_amount)

                    elif service_booking[7] in ["Paid Advance Amount", "Service Completed"]:
                        total_charge = MDLabel(
                            text=f"Total Charge: ${total_charge}",
                            theme_text_color="Custom",
                            text_color=(0.5, 0, 0.5, 1),
                            font_style="Caption",
                            size_hint_y=None,
                            height=dp(30),
                            bold=True
                        )
                        box1.add_widget(total_charge)

                        remaining_amount = MDLabel(
                            text=f"Remaining Amount: ${remaining_amount}",
                            theme_text_color="Custom",
                            text_color=(0.5, 0, 0.5, 1),
                            font_style="Caption",
                            size_hint_y=None,
                            height=dp(30),
                            bold=True
                        )
                        box1.add_widget(remaining_amount)

                    if service_booking[7] in ["Accepted Request", "Paid Advance Amount", "Service Completed"]:
                        service_booking_date = MDLabel(
                            text=f"Service Booking Date: {service_booking[4]}",
                            theme_text_color="Custom",
                            text_color=(0, 0, 0, 1),  # Black color (RGBA values)
                            font_style="Caption",
                            font_size=dp(20),  # Set the font size to 20 density-independent pixels (dp)
                            size_hint_y=None,
                            height=dp(30),
                            bold=True
                        )
                        box1.add_widget(service_booking_date)

                    if service_booking[7] in ["Paid Advance Amount", "Service Completed"] :
                        paid_amount_provider = MDLabel(
                            text=f"Paid Amount: ${service_booking[5]}",
                            theme_text_color="Custom",
                            text_color=(0, 0.5, 0, 1),  # Dark green color (RGBA values)
                            font_style="Caption",
                            size_hint_y=None,
                            height=dp(30),
                            bold=True
                        )
                        box1.add_widget(paid_amount_provider)

                    box2 = MDBoxLayout(orientation='vertical')
                    box2.add_widget(service_picture_provider)

                    cursor.execute("select * from review where service_booking_id in (select service_booking_id from service_booking where service_id = '" + str(service_id) + "')")
                    reviews = cursor.fetchall()
                    reviews = list(reviews)
                    if len(reviews) == 0:
                        no_rating = "No Rating"
                        average_rating_label = MDLabel(text=f"Rating: {no_rating}", theme_text_color="Custom",text_color=(0, 0, 0, 1))
                    else:
                        total_ratings = 0
                        number_of_ratings = 0
                        for review in reviews:
                            total_ratings = total_ratings + int(review[2])
                            number_of_ratings = number_of_ratings + 1
                        rating = total_ratings / number_of_ratings
                        rating = round(rating, 2)
                        average_rating_label = MDLabel(text=f"Rating: {rating}", theme_text_color="Custom",
                                                       text_color=(0, 0, 0, 1))
                    box2.add_widget(average_rating_label)

                    box = MDBoxLayout(orientation='horizontal')
                    box.add_widget(box1)
                    box.add_widget(box2)

                    # Add the box layout to the card
                    card.add_widget(box)

                    admin_service_cards_layout.add_widget(card)

        except Exception as e:
            print(f"An error occurred: {e}")

    def get_customer_name_from_service(customer_id):
        try:
            cursor.execute("SELECT customer_name,phone,address FROM customer WHERE customer_id = '" + str(customer_id) + "'")
            customer = cursor.fetchone()
            if customer:
                return customer[0], customer[1], customer[2]
            else:
                return None
        except Exception as e:
            print(f"Error fetching category name: {e}")
            return None

    def get_service_name_from_ProviderViewRequests(service_id):
        try:
            cursor.execute("SELECT service_name FROM service WHERE service_id = '" + str(service_id) + "'")
            service = cursor.fetchone()
            if service:
                return service[0]
            else:
                return None
        except Exception as e:
            print(f"Error fetching service name: {e}")
            return None

    def get_service_provider_details_from_service(service_id):
        try:
            cursor.execute("SELECT sp.service_provider_name, sp.email, sp.phone "
                           "FROM service s "
                           "JOIN service_provider sp ON s.service_provider_id = sp.service_provider_id "
                           "WHERE s.service_id = '" + str(service_id) + "'")
            service_provider = cursor.fetchone()
            if service_provider:
                return service_provider[0], service_provider[1], service_provider[2]
            else:
                return None
        except Exception as e:
            print(f"Error fetching service provider name: {e}")
            return None

class ViewHistoryScreen(Screen):
    def __init__(self, **kwargs):
        super(ViewHistoryScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.viewhistory_populate_table)

    def viewhistory_populate_table(self, *args):
        try:
            admin_view_history_layout = self.ids['admin_view_history_layout']
            admin_view_history_layout.clear_widgets()  # Clear existing widgets
            admin_view_history_layout.padding = [40]  # Add padding around the GridLayout
            admin_view_history_layout.spacing = 20  # Add spacing between the cards

            cursor.execute("select * from service")
            services = cursor.fetchall()
            service_ids = [service[0] for service in services]
            if service_ids:  # Check if service_ids list is not empty
                cursor.execute( "SELECT * FROM service_booking WHERE service_id IN %s AND (status = 'Request Cancelled by Customer' or status = 'Rejected Request' or status = 'Full Payment Successfull')",(tuple(service_ids),))
                view_histories = cursor.fetchall()

                if not view_histories:
                    no_requests_label = MDLabel(
                        text="No History Found",
                        font_size=30,
                        text_color=(1, 1, 1, 1),
                        theme_text_color="Custom",
                        halign="center"
                    )
                    no_requests_label.font_size = 30
                    admin_view_history_layout.add_widget(no_requests_label)
                    return

                for service_booking in view_histories:
                    service_booking_id = service_booking[0]
                    service_id = service_booking[8]
                    number_of_sq_feet = float(service_booking[1])
                    description = service_booking[2]
                    status = service_booking[7]
                    customer_id = service_booking[9]
                    booking_date = service_booking[3]

                    if status in ["Accepted Request", "Service Completed", "Paid Advance Amount"]:
                        continue  # Skip this card

                    cursor.execute("select * from service where service_id = '" + str(service_id) + "'")
                    service = cursor.fetchone()
                    service_image = service[4]
                    charger_per_sq_feet = float(service[3])

                    total_charge = number_of_sq_feet * charger_per_sq_feet
                    advance_payment = total_charge * 0.2
                    remaining_amount = total_charge - advance_payment

                    service_full_name_history = ViewHistoryScreen.get_service_by_service_id_history(service_id)

                    customer_data_history = ViewHistoryScreen.get_customer_name_from_service_history(customer_id)

                    number_of_sq_feet_history = MDLabel(text=str(number_of_sq_feet), font_size=17,
                                                        text_color=(0, 0, 0.5, 1), theme_text_color="Custom")
                    service_description_full_history = MDLabel(text=str(description), font_size=17,
                                                               text_color=(0, 0, 0.5, 1), theme_text_color="Custom")
                    service_booking_date_full_history = MDLabel(text=str(booking_date), font_size=17,
                                                                text_color=(0, 0, 0.5, 1), theme_text_color="Custom")
                    service_history = MDLabel(text=service_full_name_history, font_size=17, text_color=(0, 0, 0.5, 1),
                                              theme_text_color="Custom")
                    charger_history = MDLabel(text=f"${charger_per_sq_feet}", font_size=17, text_color=(0, 0, 0.5, 1),
                                              theme_text_color="Custom")
                    service_picture_history = AsyncImage(source=service_image, keep_ratio=True, allow_stretch=True)
                    service_status_history = MDLabel(
                        text=str(status),
                        theme_text_color="Custom",
                        text_color=(0.5, 0, 0.5, 1),  # RGB values for purple
                        bold=True,
                        font_size=17,
                    )

                    card = MDCard(
                        orientation='vertical',
                        size_hint=(None, None),
                        size=(600, 650),
                        elevation=5,
                        padding=15,
                        spacing=10,
                        md_bg_color=(0.9, 0.9, 0.9, 1)
                    )

                    box1 = MDBoxLayout(orientation='vertical')  # Add spacing between labels

                    service_name_data_history = MDLabel(
                        text="Service Name:",
                        theme_text_color="Custom",
                        font_style="Caption",
                        size_hint_y=None,
                        height=20
                    )
                    box1.add_widget(service_name_data_history)
                    box1.add_widget(service_history)

                    spacer = Widget(size_hint_y=None, height=20)
                    box1.add_widget(spacer)

                    charge_per_sq_feet_history = MDLabel(
                        text="Charger Per sq.feet:",
                        theme_text_color="Custom",
                        font_style="Caption",
                        size_hint_y=None,
                        height=20
                    )
                    box1.add_widget(charge_per_sq_feet_history)
                    box1.add_widget(charger_history)

                    spacer = Widget(size_hint_y=None, height=20)
                    box1.add_widget(spacer)

                    number_history = MDLabel(
                        text="No.of sq.feet:",
                        theme_text_color="Custom",
                        font_style="Caption",
                        size_hint_y=None,
                        height=20
                    )
                    box1.add_widget(number_history)
                    box1.add_widget(number_of_sq_feet_history)

                    spacer = Widget(size_hint_y=None, height=20)
                    box1.add_widget(spacer)

                    description_history = MDLabel(
                        text="Description:",
                        theme_text_color="Custom",
                        font_style="Caption",
                        size_hint_y=None,
                        height=20
                    )
                    box1.add_widget(description_history)
                    box1.add_widget(service_description_full_history)

                    spacer = Widget(size_hint_y=None, height=20)
                    box1.add_widget(spacer)

                    booking_date_history = MDLabel(
                        text="Booking Date:",
                        theme_text_color="Custom",
                        font_style="Caption",
                        size_hint_y=None,
                        height=20
                    )
                    box1.add_widget(booking_date_history)
                    box1.add_widget(service_booking_date_full_history)

                    spacer = Widget(size_hint_y=None, height=20)
                    box1.add_widget(spacer)

                    if service_booking[7] in ["Request Cancelled by Customer", "Rejected Request",
                                              "Full Payment Successfull"]:
                        customer_status_history = MDLabel(
                            text="Status:",
                            theme_text_color="Custom",
                            font_style="Caption",
                            size_hint_y=None,
                            height=20
                        )
                        box1.add_widget(customer_status_history)

                        spacer = Widget(size_hint_y=None, height=20)
                        box1.add_widget(spacer)

                        box1.add_widget(service_status_history)

                    spacer = Widget(size_hint_y=None, height=30)
                    box1.add_widget(spacer)

                    Customer_Details = MDLabel(
                        text="Customer Details",
                        theme_text_color="Custom",
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30)
                    )
                    box1.add_widget(Customer_Details)

                    box1.add_widget(Widget(size_hint_y=None, height=10))  # Adjust the height value as needed

                    if customer_data_history is not None:
                        customer_name_history = customer_data_history[0]  # Access the customer name
                        phone_number_history = customer_data_history[1]  # Access the phone number
                        address_history = customer_data_history[2]
                        customer_name_data_label_history = MDLabel(
                            text=f"Name: {customer_name_history}",
                            font_size=13,
                            text_color=(0, 0, 0.5, 1),
                            theme_text_color="Custom"
                        )
                        box1.add_widget(customer_name_data_label_history)

                        box1.add_widget(Widget(size_hint_y=None, height=25))  # Adjust the height value as needed

                        customer_phone_data_label_history = MDLabel(
                            text=f"Phone: {phone_number_history}",
                            font_size=13,
                            text_color=(0, 0, 0.5, 1),
                            theme_text_color="Custom"
                        )
                        box1.add_widget(customer_phone_data_label_history)

                        box1.add_widget(Widget(size_hint_y=None, height=25))  # Adjust the height value as needed

                        customer_address_label_history = MDLabel(
                            text=f"Address: {address_history}",
                            font_size=13,
                            text_color=(0, 0, 0.5, 1),
                            theme_text_color="Custom"
                        )
                        box1.add_widget(customer_address_label_history)
                    else:
                        print("No matching customer found.")

                    box1.add_widget(Widget(size_hint_y=None, height=25))  # Adjust the height value as needed

                    if service_booking[7] == "Full Payment Successfull":
                        total_charge = MDLabel(
                            text=f"Total Charge: ${total_charge}",
                            theme_text_color="Custom",
                            text_color=(0.5, 0, 0.5, 1),
                            font_style="Caption",
                            size_hint_y=None,
                            height=dp(30),
                            bold=True
                        )
                        box1.add_widget(total_charge)

                        advance_amount = MDLabel(
                            text=f"Advance Amount: ${advance_payment}",
                            theme_text_color="Custom",
                            text_color=(0.5, 0, 0.5, 1),
                            font_style="Caption",
                            size_hint_y=None,
                            height=dp(30),
                            bold=True
                        )
                        box1.add_widget(advance_amount)

                        remaining_amount = MDLabel(
                            text=f"Remaining Amount: ${remaining_amount}",
                            theme_text_color="Custom",
                            text_color=(0.5, 0, 0.5, 1),
                            font_style="Caption",
                            size_hint_y=None,
                            height=dp(30),
                            bold=True
                        )
                        box1.add_widget(remaining_amount)

                        service_date_label = MDLabel(
                            text=f"Service Done On: {service_booking[4]}",
                            theme_text_color="Custom",
                            text_color=(0, 0, 0, 1),
                            font_style="Caption",
                            size_hint_y=None,
                            height=dp(30),
                            bold=True
                        )
                        box1.add_widget(service_date_label)

                    box2 = MDBoxLayout(orientation='vertical')
                    box2.add_widget(service_picture_history)

                    cursor.execute("select * from review where service_booking_id in (select service_booking_id from service_booking where service_id = '" + str(service_id) + "')")
                    reviews = cursor.fetchall()
                    reviews = list(reviews)
                    if len(reviews) == 0:
                        no_rating = "No Rating"
                        average_rating_label = MDLabel(text=f"Rating: {no_rating}", theme_text_color="Custom",
                                                       text_color=(0, 0, 0, 1))
                    else:
                        total_ratings = 0
                        number_of_ratings = 0
                        for review in reviews:
                            total_ratings = total_ratings + int(review[2])
                            number_of_ratings = number_of_ratings + 1
                        rating = total_ratings / number_of_ratings
                        rating = round(rating, 2)
                        average_rating_label = MDLabel(text=f"Rating: {rating}", theme_text_color="Custom",
                                                       text_color=(0, 0, 0, 1))
                    box2.add_widget(average_rating_label)

                    if service_booking[7] == "Full Payment Successfull":
                        button_box = MDBoxLayout(orientation='vertical')
                        view_payment = MDRectangleFlatButton(
                            text="View Payment",
                            on_press=self.on_view_payment_press,
                            md_bg_color=get_color_from_hex("#006400"),  # Hexadecimal color for dark green
                            text_color=(1, 1, 1, 1),  # White color (RGBA values)
                        )
                        view_payment.service_booking_id = service_booking_id
                        button_box.add_widget(view_payment)

                        spacer = Widget(size_hint_y=None, height=20)  # Adjust height as needed
                        button_box.add_widget(spacer)

                        view_complaints = MDRectangleFlatButton(
                            text="View Customer Complaints",
                            on_press=self.on_view_customer_complaint_press,
                            md_bg_color=get_color_from_hex("#008080"),  # Hexadecimal color for red
                            text_color=(1, 1, 1, 1),  # White color (RGBA values)
                        )
                        view_complaints.service_booking_id = service_booking_id

                        cursor.execute("SELECT COUNT(*) FROM complaints ""WHERE service_booking_id = '" + str(service_booking_id) + "'")
                        count = cursor.fetchone()[0]
                        if count > 0:
                            button_box.add_widget(view_complaints)
                        else:
                            button_box.remove_widget(view_complaints)

                        spacer = Widget(size_hint_y=None, height=20)  # Adjust height as needed
                        button_box.add_widget(spacer)

                        view_my_complaints = MDRectangleFlatButton(
                            text="View Provider Complaints",
                            on_press=self.on_view_provider_my_complaint_press,
                            md_bg_color=get_color_from_hex("#FF5733"),  # Hexadecimal color for red
                            text_color=(1, 1, 1, 1),  # White color (RGBA values)
                            size_hint=(None, None),  # Specify size hint
                            size=(40, 40),  # Set fixed size
                            font_size='12sp',
                        )
                        view_my_complaints.service_booking_id = service_booking_id

                        cursor.execute("SELECT COUNT(*) FROM complaints ""WHERE service_booking_id = '" + str(service_booking_id) + "'")
                        count = cursor.fetchone()[0]
                        if count > 0:
                            button_box.add_widget(view_my_complaints)
                        else:
                            button_box.remove_widget(view_my_complaints)

                        box2.add_widget(button_box)

                    box = MDBoxLayout(orientation='horizontal')
                    box.add_widget(box1)
                    box.add_widget(box2)

                    # Add the box layout to the card
                    card.add_widget(box)

                    admin_view_history_layout.add_widget(card)

        except Exception as e:
            print(f"Error fetching service provider history requests: {e}")

    def on_view_payment_press(self, instance):
        service_booking_id = instance.service_booking_id
        view_payment_screen = self.manager.get_screen('view_payments_screen')
        view_payment_screen.service_booking_id = service_booking_id
        self.manager.current = 'view_payments_screen'

    def on_view_customer_complaint_press(self, instance):
        service_booking_id = instance.service_booking_id
        view_complaint_screen = self.manager.get_screen('view_customer_complaint')
        view_complaint_screen.service_booking_id = service_booking_id
        self.manager.current = 'view_customer_complaint'

    def on_view_provider_my_complaint_press(self, instance):
        service_booking_id = instance.service_booking_id
        view_my_complaint_screen = self.manager.get_screen('view_provider_complaint')
        view_my_complaint_screen.service_booking_id = service_booking_id
        self.manager.current = 'view_provider_complaint'


    def get_service_by_service_id_history(service_id):
        try:
            cursor.execute("SELECT service_name FROM service WHERE service_id = '" + str(service_id) + "'")
            service = cursor.fetchone()
            if service:
                return service[0]
            else:
                return None
        except Exception as e:
            print(f"Error fetching service name: {e}")
            return None

    def get_customer_name_from_service_history(customer_id):
        try:
            cursor.execute("SELECT customer_name,phone,address FROM customer WHERE customer_id = '" + str(customer_id) + "'")
            customer = cursor.fetchone()
            if customer:
                return customer[0], customer[1], customer[2]
            else:
                return None
        except Exception as e:
            print(f"Error fetching category name: {e}")
            return None

class ViewPaymentsScreen(Screen):

    def on_enter(self):
        try:
            view_payment_layout = self.ids['view_payment_layout']
            view_payment_layout.clear_widgets()  # Clear existing widgets
            view_payment_layout.padding = [40]  # Add padding around the GridLayout
            view_payment_layout.spacing = 20  # Add spacing between the cards

            service_booking_id = self.service_booking_id

            cursor.execute("select * from customer")
            customer = cursor.fetchone()
            customer_id = customer[0]

            cursor.execute("select * from payments where service_booking_id = '" + str(service_booking_id) + "'")
            payment = cursor.fetchone()
            print(payment)
            card_type = payment[1]
            advance_amount = payment[2]
            advance_amount_date = payment[5]
            remaining_amount = payment[3]
            remaining_amount_date = payment[6]
            total_amount = payment[4]
            status = payment[7]

            customer_details = ViewPaymentsScreen.get_customer_name_from_customer(customer_id)

            card = MDCard(
                orientation='vertical',
                size_hint=(None, None),
                size=(400, 350),
                elevation=5,  # Add elevation for shadow effect
                padding=10
            )

            Customer_Details = MDLabel(
                text="Payment Details",
                theme_text_color="Custom",
                text_color=(1, 0.647, 0, 1),  # Orange color (RGBA values)
                font_size='22',  # Adjust font size
                font_style="Caption",
                size_hint_y=None,  # Fixed height
                height=30,  # Set the height of the label
                bold=True,
                halign='center'
            )
            Customer_Details.font_size = 22
            card.add_widget(Customer_Details)

            spacer = Widget(size_hint_y=None, height=22)  # Adjust height as needed
            card.add_widget(spacer)

            if customer_details is not None:
                customer_name = customer_details[0]  # Access the customer name
                phone_number = customer_details[1]  # Access the phone number

                customer_name_data_label = MDLabel(
                    text=f"Customer Name: {customer_name}",
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    font_size='24sp',  # Adjust font size
                    font_style="Caption",
                    size_hint_y=None,  # Fixed height
                    height=30,
                    halign='center'  # Set the height of the label
                )
                card.add_widget(customer_name_data_label)

                customer_phone_data_label = MDLabel(
                    text=f"Phone Number: {phone_number}",
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    font_size='24sp',  # Adjust font size
                    font_style="Caption",
                    size_hint_y=None,  # Fixed height
                    height=30,
                    halign='center'  # Set the height of the label
                )
                card.add_widget(customer_phone_data_label)
            else:
                print("No matching customer found.")

            spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
            card.add_widget(spacer)

            card_type = MDLabel(
                text=f"Card Type: {card_type}",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                font_size='24sp',  # Adjust font size
                font_style="Caption",
                size_hint_y=None,  # Fixed height
                height=30,  # Set the height of the label
                bold=True,
                halign='center'
            )
            card.add_widget(card_type)

            spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
            card.add_widget(spacer)

            total_amount = MDLabel(
                text=f"Total Amount: ${total_amount}",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                font_size='24sp',  # Adjust font size
                font_style="Caption",
                size_hint_y=None,  # Fixed height
                height=30,  # Set the height of the label
                bold=True,
                halign='center'
            )
            card.add_widget(total_amount)

            spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
            card.add_widget(spacer)

            advance_amount = MDLabel(
                text=f"Advance Amount Paid On: ${advance_amount}({advance_amount_date})",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                font_size='24sp',  # Adjust font size
                font_style="Caption",
                size_hint_y=None,  # Fixed height
                height=30,  # Set the height of the label
                bold=True,
                halign='center'
            )
            card.add_widget(advance_amount)

            spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
            card.add_widget(spacer)

            remaining_amount = MDLabel(
                text=f"Remaining Amount Paid On: ${remaining_amount}({remaining_amount_date})",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                font_size='24sp',  # Adjust font size
                font_style="Caption",
                size_hint_y=None,  # Fixed height
                height=30,  # Set the height of the label
                bold=True,
                halign='center'
            )
            card.add_widget(remaining_amount)

            spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
            card.add_widget(spacer)

            Status = MDLabel(
                text=f"Status: {status}",
                theme_text_color="Custom",
                text_color=(0, 0.392, 0, 1),  # Dark Green color (RGBA values)
                font_style="Caption",
                font_size='50sp',  # Adjust font size to be extra large
                size_hint_y=None,  # Fixed height
                height=30,  # Set the height of the label
                bold=True,
                halign='center'
            )
            card.add_widget(Status)

            view_payment_layout.add_widget(card)

        except Exception as e:
            print(f"Error fetching payments: {e}")

    def get_customer_name_from_customer(customer_id):
        try:
            cursor.execute("SELECT customer_name,phone FROM customer WHERE customer_id = '" + str(customer_id) + "'")
            customer = cursor.fetchone()
            if customer:
                return customer[0], customer[1]
            else:
                return None
        except Exception as e:
            print(f"Error fetching category name: {e}")
            return None

class ViewCustomerComplaintsScreen(Screen):

    def on_enter(self):
        try:
            view_complaints_screen = self.ids['view_complaints_screen']
            view_complaints_screen.clear_widgets()  # Clear existing widgets
            view_complaints_screen.padding = [40]  # Add padding around the GridLayout
            view_complaints_screen.spacing = 20  # Add spacing between the cards

            service_booking_id = self.service_booking_id

            cursor.execute("select * from customer")
            customer = cursor.fetchone()
            customer_id = customer[0]

            card = MDCard(
                orientation='vertical',
                size_hint=(None, None),
                size=(400, 300),
                elevation=5,  # Add elevation for shadow effect
                padding=10
            )

            cursor.execute("select * from complaints where service_booking_id = '" + str(service_booking_id) + "' and customer_id = '" + str(customer_id) + "'")
            complaint = cursor.fetchone()
            status = complaint[1]
            complaint_description = complaint[2]

            complaint_description_label = MDLabel(text=str(complaint_description), theme_text_color="Custom",
                                                  text_color=(1, 1, 1, 1),
                                                  halign='center',
                                                  font_size='24sp',  # Adjust font size
                                                  font_style="Caption",
                                                  size_hint_y=None,  # Fixed height
                                                  height=30,  # Set the height of the label
                                                  )

            customer_details_table = ViewCustomerComplaintsScreen.get_customer_name_from_customer_table(customer_id)

            Customer_Details = MDLabel(
                text="View Customer Complaints",
                theme_text_color="Custom",
                text_color=(1, 0.647, 0, 1),
                font_size='22',  # Adjust font size
                font_style="Caption",
                size_hint_y=None,  # Fixed height
                height=30,  # Set the height of the label
                bold=True,
                halign='center'
            )
            Customer_Details.font_size = 22
            card.add_widget(Customer_Details)

            spacer = Widget(size_hint_y=None, height=22)  # Adjust height as needed
            card.add_widget(spacer)

            if customer_details_table is not None:
                customer_name = customer_details_table[0]  # Access the customer name
                phone_number = customer_details_table[1]  # Access the phone number

                customer_name_data_label = MDLabel(
                    text=f"Customer Name: {customer_name}",
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    font_size='24sp',  # Adjust font size
                    font_style="Caption",
                    size_hint_y=None,  # Fixed height
                    height=30,
                    halign='center'
                )
                card.add_widget(customer_name_data_label)

                customer_phone_data_label = MDLabel(
                    text=f"Phone Number: {phone_number}",
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    font_size='24sp',  # Adjust font size
                    font_style="Caption",
                    halign='center',
                    size_hint_y=None,  # Fixed height
                    height=30,  # Set the height of the label
                )
                card.add_widget(customer_phone_data_label)
            else:
                print("No matching customer found.")

            spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
            card.add_widget(spacer)

            Compalint = MDLabel(
                text="Complaint:",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                font_size='24sp',  # Adjust font size
                font_style="Caption",
                halign='center',
                size_hint_y=None,  # Fixed height
                height=30,  # Set the height of the label
                bold=True
            )
            card.add_widget(Compalint)
            card.add_widget(complaint_description_label)

            spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
            card.add_widget(spacer)

            Status = MDLabel(
                text=f"Status: {status}",
                theme_text_color="Custom",
                text_color=(0, 0.392, 0, 1),  # Dark Green color (RGBA values)
                font_style="Caption",
                halign='center',
                font_size='20',  # Adjust font size to be extra large
                size_hint_y=None,  # Fixed height
                height=30,  # Set the height of the label
                bold=True
            )
            Status.font_size = 20
            card.add_widget(Status)

            spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
            card.add_widget(spacer)

            view_complaints_screen.add_widget(card)

        except Exception as e:
            print(f"Error fetching customer complaints: {e}")

    def get_customer_name_from_customer_table(customer_id):
        try:
            cursor.execute("SELECT customer_name,phone FROM customer WHERE customer_id = '" + str(customer_id) + "'")
            customer = cursor.fetchone()
            if customer:
                return customer[0], customer[1]
            else:
                return None
        except Exception as e:
            print(f"Error fetching category name: {e}")
            return None

class ViewProviderComplaintsScreen(Screen):

    def on_enter(self):
        try:
            view_provider_complaints_screen = self.ids['view_provider_complaints_screen']
            view_provider_complaints_screen.clear_widgets()  # Clear existing widgets
            view_provider_complaints_screen.padding = [40]  # Add padding around the GridLayout
            view_provider_complaints_screen.spacing = 20  # Add spacing between the cards

            service_booking_id = self.service_booking_id

            cursor.execute("select * from service_provider")
            service_provider = cursor.fetchone()
            service_provider_id = service_provider[0]

            cursor.execute("select * from complaints where service_booking_id = '" + str(service_booking_id) + "' and service_provider_id = '" + str(service_provider_id) + "'")
            complaint = cursor.fetchone()
            status = complaint[1]
            complaint_description = complaint[2]

            card = MDCard(
                orientation='vertical',
                size_hint=(None, None),
                size=(400, 250),
                elevation=5,  # Add elevation for shadow effect
                padding=10
            )

            My_Compalint = MDLabel(
                text="View Provider Complaint",
                theme_text_color="Custom",
                text_color=(1, 0.647, 0, 1),
                font_size='22',  # Adjust font size
                font_style="Caption",
                size_hint_y=None,  # Fixed height
                height=30,  # Set the height of the label
                bold=True,
                halign='center'
            )
            My_Compalint.font_size = 22
            card.add_widget(My_Compalint)

            spacer = Widget(size_hint_y=None, height=30)  # Adjust height as needed
            card.add_widget(spacer)

            Compalint = MDLabel(
                text=f"Compalint: {complaint_description}",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),  # Black color (RGBA values)
                font_size='24sp',  # Adjust font size
                font_style="Caption",
                size_hint_y=None,  # Fixed height
                height=30,  # Set the height of the label
                bold=True,
                halign='center'
            )
            card.add_widget(Compalint)

            spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
            card.add_widget(spacer)

            Status = MDLabel(
                text=f"Status: {status}",
                theme_text_color="Custom",
                text_color=(0, 0.392, 0, 1),  # Dark Green color (RGBA values)
                font_style="Caption",
                font_size='20',  # Adjust font size to be extra large
                size_hint_y=None,  # Fixed height
                height=30,  # Set the height of the label
                bold=True,
                halign='center'
            )
            Status.font_size = 20
            card.add_widget(Status)

            view_provider_complaints_screen.add_widget(card)

        except Exception as e:
            print(f"Error fetching provider complaints: {e}")

class SnowRemovalApp(MDApp):

    def build(self):
        Window.size = (360, 640)

        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.primary_hue = "100"

        # Set theme text color to white
        self.theme_cls.theme_style = "Dark"  # Set theme style to dark
        self.theme_cls.primary_style = "Light"  # Set primary style to light

        # Set the font family
        self.theme_cls.font_styles.update({
            "H1": ["comic.ttf", 96, False, -1.5],
            "H2": ["comic.ttf", 60, False, -0.5],
            "H3": ["comic.ttf", 48, False, 0],
            "H4": ["comic.ttf", 34, False, 0.25],
            "H5": ["comic.ttf", 24, False, 0],
            "H6": ["comic.ttf", 20, False, 0.15],
            "Subtitle1": ["comic.ttf", 16, False, 0.15],
            "Subtitle2": ["comic.ttf", 14, False, 0.1],
            "Body1": ["comic.ttf", 16, False, 0.5],
            "Body2": ["comic.ttf", 14, False, 0.25],
            "Button": ["comic.ttf", 14, True, 1.25],
            "Caption": ["comic.ttf", 12, False, 0.4],
            "Overline": ["comic.ttf", 10, True, 1.5],
        })

        root = MDBoxLayout(orientation='vertical', size_hint=(1, 1))  # Take up full available space

        self.bg = Image(source='static/myfiles/17.jpg', allow_stretch=True, size=(900, 900))  # Set the desired size

        # Add a Canvas with the background image
        with root.canvas.before:
            Rectangle(texture=self.bg.texture, size=self.bg.texture.size, pos=root.pos)

        def update_bg_size(instance, value):
            self.bg.size = value
            self.bg.pos = instance.pos

        root.bind(size=update_bg_size)

        screen_nav = Builder.load_string(screen_helper)
        self.manager = ScreenManager(transition=NoTransition())
        self.manager.add_widget(HomeScreen(name="home_screen"))
        self.manager.add_widget(AdminLoginScreen(name="admin_login_screen"))
        self.manager.add_widget(AdminHomeScreen(name="adminhome"))
        self.manager.add_widget(AddLocationScreen(name="add_location_screen"))
        self.manager.add_widget(ViewLocationScreen(name="view_location_screen"))
        self.manager.add_widget(AddCategoryScreen(name="add_category_screen"))
        self.manager.add_widget(ViewCategoryScreen(name="view_category_screen"))
        self.manager.add_widget(ViewProvidersScreen(name="view_providers_screen"))
        self.manager.add_widget(ViewRequestScreen(name="view_request_screen"))
        self.manager.add_widget(ViewHistoryScreen(name="view_history_screen"))
        self.manager.add_widget(ViewPaymentsScreen(name="view_payments_screen"))
        self.manager.add_widget(ViewCustomerComplaintsScreen(name="view_customer_complaint"))
        self.manager.add_widget(ViewProviderComplaintsScreen(name="view_provider_complaint"))


        root.add_widget(self.manager)

        return root


if __name__ == "__main__":
    SnowRemovalApp().run()