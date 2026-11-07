from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Page Object untuk halaman Inventory/Products setelah login berhasil."""
    
    # =========================================================================
    # ELEMEN LOKATOR (Relative XPath)
    # =========================================================================
    PAGE_TITLE = (By.XPATH, "//span[@class='title' and text()='Products']")
    
    ADD_BACKPACK_BTN = (
        By.XPATH,
        "//button[contains(@data-test, 'add-to-cart-sauce-labs-backpack')]"
    )
    
    CART_BADGE = (By.XPATH, "//span[@class='shopping_cart_badge']")
    
    BURGER_MENU_BTN = (By.XPATH, "//button[@id='react-burger-menu-btn']")
    
    LOGOUT_LINK = (By.XPATH, "//a[@id='logout_sidebar_link']")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    # =========================================================================
    # METHODS / ACTIONS
    # =========================================================================
    def is_inventory_page_displayed(self) -> bool:
        return self.find_element(self.PAGE_TITLE).is_displayed()
    
    def add_backpack_to_cart(self):
        self.click(self.ADD_BACKPACK_BTN)
    
    def get_cart_badge_count(self) -> str:
        return self.get_text(self.CART_BADGE)
    
    def is_cart_badge_visible(self) -> bool:
        return self.find_element(self.CART_BADGE).is_displayed()
    
    def logout(self):
        """
        Alur logout yang tahan banting (robust) terhadap animasi React.
        1. Klik burger menu.
        2. Tunggu elemen Logout benar-benar VISIBLE (menjamin animasi sidebar selesai).
        3. Klik elemen Logout (method self.click di BasePage sudah menangani element_to_be_clickable).
        """
        # Langkah 1: Klik burger menu
        self.click(self.BURGER_MENU_BTN)
        
        # Langkah 2: Tunggu sampai link Logout benar-benar muncul di layar (visible)
        # Ini adalah kunci agar tidak gagal klik karena animasi yang belum selesai
        self.wait.until(EC.visibility_of_element_located(self.LOGOUT_LINK))
        
        # Langkah 3: Klik logout (menggunakan method click dari BasePage yang sudah 
        # memiliki explicit wait untuk element_to_be_clickable)
        self.click(self.LOGOUT_LINK)