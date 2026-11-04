import data
import helpers
from selenium import webdriver
from pages import UrbanRoutesPage


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        # Verifica se o servidor Urban Routes está ativo antes de executar os testes
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Conectado ao servidor Urban Routes")
        else:
            print("Não foi possível conectar ao Urban Routes. Verifique se o servidor está ligado e ainda em execução.")

        # não modifique, pois precisamos do registro adicional habilitado para recuperar o código de confirmação do telefone
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        # No Selenium 4 as capabilities precisam ser passadas pelas opções do Chrome
        options = webdriver.ChromeOptions()
        options.set_capability("goog:loggingPrefs", capabilities["goog:loggingPrefs"])
        cls.driver = webdriver.Chrome(options=options)

    def open_page(self):
        # Abre a página inicial e define a rota, passo comum a todos os testes
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        return routes_page

    def test_set_route(self):
        routes_page = self.open_page()
        assert routes_page.get_from() == data.ADDRESS_FROM
        assert routes_page.get_to() == data.ADDRESS_TO

    def test_select_plan(self):
        routes_page = self.open_page()
        routes_page.select_comfort_plan()
        assert routes_page.get_selected_plan() == 'Comfort'

    def test_fill_phone_number(self):
        routes_page = self.open_page()
        routes_page.select_comfort_plan()
        routes_page.fill_phone_number(data.PHONE_NUMBER)
        assert routes_page.get_phone_number() == data.PHONE_NUMBER

    def test_fill_card(self):
        routes_page = self.open_page()
        routes_page.select_comfort_plan()
        routes_page.add_card(data.CARD_NUMBER, data.CARD_CODE)
        assert routes_page.get_payment_method() == 'Cartão'

    def test_comment_for_driver(self):
        routes_page = self.open_page()
        routes_page.select_comfort_plan()
        routes_page.set_comment(data.MESSAGE_FOR_DRIVER)
        assert routes_page.get_comment() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        routes_page = self.open_page()
        routes_page.select_comfort_plan()
        routes_page.order_blanket_and_handkerchiefs()
        assert routes_page.is_blanket_selected()

    def test_order_2_ice_creams(self):
        routes_page = self.open_page()
        routes_page.select_comfort_plan()
        routes_page.order_ice_creams(2)
        assert routes_page.get_ice_cream_count() == 2

    def test_car_search_model_appears(self):
        routes_page = self.open_page()
        routes_page.select_comfort_plan()
        routes_page.fill_phone_number(data.PHONE_NUMBER)
        routes_page.set_comment(data.MESSAGE_FOR_DRIVER)
        routes_page.order_taxi()
        assert routes_page.is_car_search_modal_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
