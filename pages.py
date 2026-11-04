from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import helpers


class UrbanRoutesPage:
    # Endereços
    FROM_FIELD = (By.ID, 'from')
    TO_FIELD = (By.ID, 'to')

    # Tarifas
    CALL_TAXI_BUTTON = (By.XPATH, '//button[text()="Chamar um táxi"]')
    COMFORT_TARIFF = (By.XPATH, '//div[contains(@class, "tcard")][.//div[text()="Comfort"]]')
    ACTIVE_TARIFF_TITLE = (By.CSS_SELECTOR, '.tcard.active .tcard-title')

    # Telefone
    PHONE_NUMBER_BUTTON = (By.CLASS_NAME, 'np-button')
    PHONE_NUMBER_TEXT = (By.CLASS_NAME, 'np-text')
    PHONE_INPUT = (By.ID, 'phone')
    NEXT_BUTTON = (By.XPATH, '//button[text()="Próximo"]')
    SMS_CODE_INPUT = (By.XPATH, '//div[@class="np-input"]//input[@id="code"]')
    CONFIRM_BUTTON = (By.XPATH, '//button[text()="Confirmar"]')

    # Cartão
    PAYMENT_METHOD_BUTTON = (By.CLASS_NAME, 'pp-button')
    ADD_CARD_OPTION = (By.XPATH, '//div[@class="pp-title" and text()="Adicionar cartão"]')
    CARD_NUMBER_INPUT = (By.ID, 'number')
    CARD_CODE_INPUT = (By.XPATH, '//input[@id="code" and @class="card-input"]')
    ADD_CARD_BUTTON = (By.XPATH, '//button[text()="Adicionar"]')
    CLOSE_PAYMENT_MODAL_BUTTON = (By.XPATH, '//div[@class="payment-picker open"]//button[@class="close-button section-close"]')
    PAYMENT_METHOD_VALUE = (By.CLASS_NAME, 'pp-value-text')

    # Comentário para o motorista
    COMMENT_INPUT = (By.ID, 'comment')

    # Cobertor e lenços: um seletor para clicar e outro para verificar o estado
    BLANKET_SLIDER = (By.XPATH, '//div[text()="Cobertor e lençóis"]/following-sibling::div//span[contains(@class, "slider")]')
    BLANKET_CHECKBOX = (By.XPATH, '//div[text()="Cobertor e lençóis"]/following-sibling::div//input[@type="checkbox"]')

    # Sorvete
    ICE_CREAM_PLUS = (By.XPATH, '//div[text()="Sorvete"]/following-sibling::div//div[@class="counter-plus"]')
    ICE_CREAM_COUNTER = (By.XPATH, '//div[text()="Sorvete"]/following-sibling::div//div[@class="counter-value"]')

    # Pedido
    ORDER_BUTTON = (By.CLASS_NAME, 'smart-button')
    CAR_SEARCH_MODAL = (By.CLASS_NAME, 'order-body')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def _find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def _click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    # Endereço
    def set_route(self, address_from, address_to):
        self._find(self.FROM_FIELD).send_keys(address_from)
        self._find(self.TO_FIELD).send_keys(address_to)

    def get_from(self):
        return self._find(self.FROM_FIELD).get_property('value')

    def get_to(self):
        return self._find(self.TO_FIELD).get_property('value')

    # Tarifa
    def select_comfort_plan(self):
        self._click(self.CALL_TAXI_BUTTON)
        comfort_card = self._find(self.COMFORT_TARIFF)
        # Só clica se o Comfort ainda não estiver selecionado, para evitar cliques desnecessários
        if 'active' not in comfort_card.get_attribute('class'):
            comfort_card.click()

    def get_selected_plan(self):
        return self._find(self.ACTIVE_TARIFF_TITLE).text

    # Telefone
    def fill_phone_number(self, phone_number):
        self._click(self.PHONE_NUMBER_BUTTON)
        self._find(self.PHONE_INPUT).send_keys(phone_number)
        self._click(self.NEXT_BUTTON)
        # Espera o campo do SMS aparecer, o que indica que o código já foi solicitado
        sms_input = self._find(self.SMS_CODE_INPUT)
        code = helpers.retrieve_phone_code(self.driver)
        sms_input.send_keys(code)
        self._click(self.CONFIRM_BUTTON)

    def get_phone_number(self):
        return self._find(self.PHONE_NUMBER_TEXT).text

    # Cartão
    def add_card(self, card_number, card_code):
        self._click(self.PAYMENT_METHOD_BUTTON)
        self._click(self.ADD_CARD_OPTION)
        self._find(self.CARD_NUMBER_INPUT).send_keys(card_number)
        code_input = self._find(self.CARD_CODE_INPUT)
        code_input.send_keys(card_code)
        # O botão "Adicionar" só fica clicável depois que o campo CVV perde o foco
        code_input.send_keys(Keys.TAB)
        self._click(self.ADD_CARD_BUTTON)
        self._click(self.CLOSE_PAYMENT_MODAL_BUTTON)

    def get_payment_method(self):
        return self._find(self.PAYMENT_METHOD_VALUE).text

    # Comentário
    def set_comment(self, message):
        self._find(self.COMMENT_INPUT).send_keys(message)

    def get_comment(self):
        return self._find(self.COMMENT_INPUT).get_property('value')

    # Cobertor e lenços
    def order_blanket_and_handkerchiefs(self):
        self._click(self.BLANKET_SLIDER)

    def is_blanket_selected(self):
        return self.driver.find_element(*self.BLANKET_CHECKBOX).get_property('checked')

    # Sorvete
    def order_ice_creams(self, quantity):
        # Clica no "+" uma vez para cada sorvete
        for _ in range(quantity):
            self._click(self.ICE_CREAM_PLUS)

    def get_ice_cream_count(self):
        return int(self._find(self.ICE_CREAM_COUNTER).text)

    # Pedido
    def order_taxi(self):
        self._click(self.ORDER_BUTTON)

    def is_car_search_modal_displayed(self):
        return self._find(self.CAR_SEARCH_MODAL).is_displayed()
