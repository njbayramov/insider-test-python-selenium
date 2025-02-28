from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time

# Function to get chrome options
def get_chrome_options():
    # Set up Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return options

# Function to set driver options
def initialize_driver():
    chrome_options = get_chrome_options()
    driver = webdriver.Remote(
        command_executor="http://selenium-hub:4444/wd/hub",
        options=chrome_options
    )

    # Set Browser Window to Desktop View
    driver.set_window_size(1920, 1080)

    return driver

# Function for initialize driver 
def check_chrome():
    try:
        driver = initialize_driver()
        driver.quit()
        print("✅ Chrome is working correctly.")
    except Exception as e:
        print("❌ Chrome is not working:", str(e))
        return False
    return True

# Function to accept the cookie consent
def accept_cookie_consent(driver):
    try:
        # Wait for the cookie consent button to be clickable
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "wt-cli-accept-all-btn"))
        )

        # Scroll to the button using Selenium's ActionChains to move to it
        actions = ActionChains(driver)
        actions.move_to_element(cookie_button).perform()

        # Click the button to accept the cookie consent
        cookie_button.click()
        print("✅ Accepted cookie consent.")
    except Exception as e:
        print(f"⚠️ No cookie prompt found, continuing... Error: {str(e)}")

def test_homepage():
    try:
        # Call the function to initialize the driver
        driver = initialize_driver()

        # Load the homepage
        driver.get("https://useinsider.com/")
        assert "Insider" in driver.title
        print("✅ Insider homepage loaded successfully.")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        driver.save_screenshot("home_page_error.png")
        print("📸 Screenshot saved as 'home_page_error.png'.")
        raise
    finally:
        driver.quit()
        print("✅ Browser closed.")

def test_careers_page():
    try:
        # Step 1: Initialize the WebDriver
        driver = initialize_driver()

        # Step 2: Load Insider home page
        driver.get("https://useinsider.com/")
        print("✅ Insider homepage loaded successfully.")

        # Step 3: Handle the Cookie Consent Prompt (If present)
        accept_cookie_consent(driver)

        # Step 4: Wait for the Navbar to Load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "navbar-nav"))
        )
        print("✅ Navbar loaded successfully.")

        # Step 5: Locate and Hover Over the "Company" Menu
        company_menu = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Company')]"))
        )
        print("✅ Located the 'Company' dropdown menu.")

        # Step 6: Scroll the "Company" menu into view and hover over it
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", company_menu)
        actions = ActionChains(driver)
        actions.move_to_element(company_menu).perform()
        print("✅ Hovered over the 'Company' menu.")

        # Step 7: Click on the "Careers" link under the "Company" menu
        careers_option = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'dropdown-sub') and contains(text(), 'Careers')]"))
        )
        careers_option.click()
        print("✅ Clicked on the 'Careers' option.")

        # Step 8: Verify that the Careers Page has loaded
        WebDriverWait(driver, 10).until(
            EC.url_contains("careers")
        )
        assert "careers" in driver.current_url, "❌ Careers page did not load correctly."
        print("✅ Careers page loaded successfully.")

        # Step 9: Check if the "Our Locations" section is visible
        locations_section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "career-our-location"))
        )
        assert locations_section.is_displayed(), "❌ 'Our Locations' section not visible."
        print("✅ 'Our Locations' section is visible.")

        # Step 10: Check if the "Life at Insider" section is visible
        life_at_insider_section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Life at Insider')]"))
        )
        assert life_at_insider_section.is_displayed(), "❌ 'Life at Insider' section not visible."
        print("✅ 'Life at Insider' section is visible.")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        driver.save_screenshot("careers_page_error.png")
        print("📸 Screenshot saved as 'careers_page_error.png'.")
        raise
    finally:
        driver.quit()
        print("✅ Browser closed.")

def test_qa_jobs():
    try:
        # Step 1: Initialize the WebDriver
        driver = initialize_driver()

        # Step 2: Navigate to the QA Careers Page
        driver.get("https://useinsider.com/careers/quality-assurance/")
        print("✅ QA Careers page loaded successfully.")

        # Step 3: Handle the Cookie Consent Prompt (If present)
        accept_cookie_consent(driver)            

        # Step 4: Click on "See all QA jobs" button
        see_all_qa_jobs_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'btn') and contains(text(), 'See all QA jobs')]"))
        )
        see_all_qa_jobs_button.click()
        print("✅ Clicked on 'See all QA jobs' button.")

        # Step 5: Wait for the jobs page to load by checking the URL
        WebDriverWait(driver, 10).until(
            EC.url_contains("open-positions")
        )
        print("✅ Open positions page loaded.")

        # Step 6: Apply Filters (Location: Istanbul, Turkiye and Department: Quality Assurance)
        # Location Filter
        location_filter = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//select[@id='filter-by-location']"))
        )
        # Scroll the location filter into view if it is being blocked
        driver.execute_script("arguments[0].scrollIntoView(true);", location_filter)
        # Click the dropdown to expand options
        ActionChains(driver).move_to_element(location_filter).click().perform()

        # Wait for the location options to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//select[@id='filter-by-location']//option"))
        )

        # Select Istanbul, Turkiye as the location
        istanbul_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//option[contains(text(), 'Istanbul, Turkiye')]"))
        )
        istanbul_option.click()
        print("✅ Selected Istanbul, Turkiye as location filter.")

        # Department Filter
        department_filter = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//select[@id='filter-by-department']"))
        )
        # Scroll and click the department filter
        driver.execute_script("arguments[0].scrollIntoView(true);", department_filter)
        ActionChains(driver).move_to_element(department_filter).click().perform()

        # Select Quality Assurance as the department
        qa_department_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//option[contains(text(), 'Quality Assurance')]"))
        )
        qa_department_option.click()
        print("✅ Selected Quality Assurance as department filter.")

        # Step 7: Count the job listings
        jobs_list = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located(
                (By.XPATH, "//div[contains(@class, 'position-list')]//div[contains(@class, 'position-list-item') and not(contains(@class, 'position-list-item-wrapper'))]")
            )
        )
        assert len(jobs_list) > 0, "❌ No QA jobs found after filtering."
        print(f"✅ Found {len(jobs_list)} QA jobs.")

        # Step 8: Loop through each job listing
        for job in jobs_list:
            try:
                # Extract position details
                title = job.find_element(By.CLASS_NAME, "position-title").text.strip()
                department = job.find_element(By.CLASS_NAME, "position-department").text.strip()
                location = job.find_element(By.CLASS_NAME, "position-location").text.strip()

                # Check for department and location conditions
                qa_status = "✅ Yes" if "Quality Assurance" in department else "❌ No"
                location_status = "✅ Yes" if "Istanbul, Turkiye" in location else "❌ No"

                # Print job details
                print(f"🔹 Position Title: {title}")
                print(f"   - Contains 'Quality Assurance': {qa_status}")
                print(f"   - Contains 'Istanbul, Turkiye': {location_status}")

                # Step 9: Hover over the job to reveal the "View Role" button
                actions = ActionChains(driver)
                actions.move_to_element(job).perform()

                # Find and click the "View Role" button to open the job in a new tab
                view_role_button = WebDriverWait(job, 10).until(
                    EC.element_to_be_clickable((By.XPATH, ".//a[contains(@class, 'btn') and contains(text(), 'View Role')]"))
                )
                actions.move_to_element(view_role_button).click().perform()
                time.sleep(2)  # Wait for the new tab to open

                # Step 10: Verify if a new tab is opened
                current_tabs = driver.window_handles
                if len(current_tabs) > 1:
                    print(f"   - View Role page loaded: ✅ Yes")
                    driver.switch_to.window(current_tabs[-1])

                    # Step 11: Click on the "Apply for this job" button
                    try:
                        apply_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'postings-btn') and contains(text(), 'Apply for this job')]"))
                        )
                        apply_button.click()

                        # Step 12: Check if the Lever Application Form is loaded
                        current_url = driver.current_url
                        if "lever.co" in current_url:
                            print(f"   - Lever Application form loaded: ✅ Yes")
                        else:
                            print(f"   - Lever Application form loaded: ❌ No")

                    except Exception as e:
                        print(f"   - Error clicking 'Apply for this job' for {title}: {str(e)}")

                    # Step 13: Close the job tab and switch back to the main tab
                    driver.close()
                    driver.switch_to.window(current_tabs[0])
                else:
                    print(f"   - New tab opened for {title}: ❌ No")

            except StaleElementReferenceException as e:
                print(f"   - Stale Element Reference Exception for {title}: {str(e)}")
            
            except Exception as e:
                print(f"   - Error processing position {title}: {str(e)}")
            
            print("-" * 50)
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        driver.save_screenshot("qa_jobs_error.png")
        print("📸 Screenshot saved as 'qa_jobs_error.png'.")
        raise
    finally:
        driver.quit()
        print("✅ Browser closed.")

if __name__ == "__main__":
    if check_chrome():
        test_homepage()
        test_careers_page()
        test_qa_jobs()
