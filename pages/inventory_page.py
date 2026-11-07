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
        Alur logout yang tahan banting terhadap animasi React dan Race Condition.
        """
        # 1. Klik burger menu
        self.click(self.BURGER_MENU_BTN)
        
        # 2. Tunggu tombol logout benar-benar bisa diklik (menjamin sidebar sudah terbuka)
        logout_element = self.wait.until(EC.element_to_be_clickable(self.LOGOUT_LINK))
        
        # 3. Klik menggunakan JavaScript. 
        # Ini adalah trik industri untuk menghindari masalah 'click intercepted' 
        # oleh animasi/overlay sidebar yang sering terjadi di React.
        self.driver.execute_script("arguments[0].click();", logout_element)
        
        # 4. KRUSIAL: Tunggu secara eksplisit sampai URL benar-benar berubah ke halaman login.
        # Ini mencegah test membaca URL sebelum proses redirect selesai (Race Condition).
        self.wait.until(lambda driver: driver.current_url == "https://www.saucedemo.com/")