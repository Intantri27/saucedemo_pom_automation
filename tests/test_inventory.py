import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


class TestInventory:
    """Kumpulan kasus uji untuk alur inventori dan keranjang belanja."""
    
    def test_add_to_cart_flow(self, driver):
        """
        TC-01: Add to Cart Flow
        
        Langkah:
          1. Login sebagai standard_user
          2. Tambahkan produk 'Sauce Labs Backpack' ke keranjang
          3. Validasi badge keranjang menunjukkan angka '1'
        """
        # === Arrange ===
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")
        
        inventory_page = InventoryPage(driver)
        
        # === Act ===
        inventory_page.add_backpack_to_cart()
        
        # === Assertions ===
        # Assertion 1: Badge keranjang harus terlihat
        assert inventory_page.is_cart_badge_visible() is True, (
            "Badge keranjang belanja tidak muncul setelah menambah produk!"
        )
        
        # Assertion 2: Badge harus menunjukkan angka '1'
        badge_count = inventory_page.get_cart_badge_count()
        assert badge_count == "1", (
            f"Jumlah di badge salah. Diharapkan '1', diterima: '{badge_count}'"
        )
    
    def test_logout_flow(self, driver):
        """
        TC-02: Logout Flow
        
        Langkah:
          1. Login sebagai standard_user
          2. Buka burger menu, klik Logout
          3. Validasi dialihkan kembali ke halaman login
          4. Validasi tombol login kembali tampil
        """
        # === Arrange ===
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")
        
        inventory_page = InventoryPage(driver)
        
        # === Act ===
        inventory_page.logout()
        
        # === Assertions ===
        # Assertion 1: URL harus kembali ke halaman login
        expected_login_url = "https://www.saucedemo.com/"
        actual_url = login_page.get_current_url()
        assert actual_url == expected_login_url, (
            f"Gagal logout. Diharapkan URL '{expected_login_url}', tetapi berada di '{actual_url}'"
        )
        
        # Assertion 2: Tombol login harus kembali tampil
        login_button_visible = driver.find_element(
            *LoginPage.LOGIN_BUTTON
        ).is_displayed()
        assert login_button_visible is True, (
            "Tombol Login tidak tampil setelah logout!"
        )