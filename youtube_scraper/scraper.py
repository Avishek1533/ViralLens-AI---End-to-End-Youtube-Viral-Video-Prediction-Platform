import os
import time
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import datetime

# Target number of videos
TARGET_VIDEOS = 15000
MIN_VIEWS = 10000000
MIN_YEAR = 2020
MAX_YEAR = 2026

EXCEL_FILE = "youtube_data.xlsx"

def setup_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def safe_save(results_list, filename):
    for attempt in range(5):
        try:
            pd.DataFrame(results_list).to_excel(filename, index=False)
            return
        except PermissionError:
            print(f"File {filename} is open. Please close it! Retrying in 10s...")
            time.sleep(10)
        except Exception as e:
            print(f"Save error: {e}")
            break

def get_video_details(driver, url):
    driver.get(url)
    time.sleep(3)
    
    driver.execute_script("window.scrollBy(0, 600);")
    time.sleep(2)
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(3)
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    data = {
        "URL": url,
        "Title": "",
        "Description": "",
        "Likes": "",
        "Comments": "",
        "Views": 0,
        "Duration_Sec": 0,
        "Tags": "",
        "Upload_Date": "",
        "Thumbnail_URL": ""
    }
    
    # 1. Title
    title_element = soup.find("meta", {"name": "title"})
    if title_element:
        data["Title"] = title_element.get("content", "")
        
    # 2. Upload Date
    upload_date_elem = soup.find("meta", {"itemprop": "uploadDate"})
    if upload_date_elem:
        data["Upload_Date"] = upload_date_elem.get("content", "")[:10]
    else:
        date_match = re.search(r'"publishDate":"(\d{4}-\d{2}-\d{2})"', driver.page_source)
        if date_match:
            data["Upload_Date"] = date_match.group(1)
            
    # 3. Views
    views_elem = soup.find("meta", {"itemprop": "interactionCount"})
    if views_elem:
        try:
            data["Views"] = int(views_elem.get("content", "0"))
        except:
            pass
    if data["Views"] == 0:
        views_match = re.search(r'"viewCount":"(\d+)"', driver.page_source)
        if views_match:
            data["Views"] = int(views_match.group(1))

    # 4. Duration
    duration_match = re.search(r'"lengthSeconds":"(\d+)"', driver.page_source)
    if duration_match:
        data["Duration_Sec"] = int(duration_match.group(1))

    # 5. Tags
    tags = []
    for tag_elem in soup.find_all("meta", {"property": "og:video:tag"}):
        tags.append(tag_elem.get("content", ""))
    data["Tags"] = ", ".join(tags)

    # 6. Thumbnail URL
    thumb_elem = soup.find("meta", {"property": "og:image"})
    if thumb_elem:
        data["Thumbnail_URL"] = thumb_elem.get("content", "")
        
    # 7. Description
    desc_elem = soup.find("meta", {"property": "og:description"})
    if desc_elem:
        data["Description"] = desc_elem.get("content", "")
        
    # 8. Likes
    try:
        like_btn = driver.find_element(By.XPATH, '//*[@id="top-level-buttons-computed"]//button[contains(@aria-label, "like this video")]')
        aria_label = like_btn.get_attribute('aria-label')
        likes_match = re.search(r'along with ([\d,]+) other people', aria_label)
        if likes_match:
            data["Likes"] = likes_match.group(1)
        else:
            data["Likes"] = aria_label
    except Exception:
        pass

    # 9. Comments
    try:
        comments_elem = driver.find_element(By.XPATH, '//*[@id="count"]//*[@dir="auto"]')
        data["Comments"] = comments_elem.text
    except Exception:
        pass

    return data

def build_queries():
    base_topics = ["music", "gaming", "news", "vlog", "podcast", "documentary", "mrbeast", "movie trailers", "funny videos", "science", "math", "sports", "football", "cricket", "basketball", "reaction", "prank", "cooking", "travel"]
    years = [2020, 2021, 2022, 2023, 2024, 2025, 2026]
    queries = []
    for topic in base_topics:
        for year in years:
            queries.append(f"{topic} {year}")
    
    # Also sort by view count for generic search terms
    for topic in base_topics:
        queries.append(f"{topic} highly viewed")
    
    return queries

def main():
    if os.path.exists(EXCEL_FILE):
        df_existing = pd.read_excel(EXCEL_FILE)
        scraped_urls = set(df_existing["URL"].tolist())
        results = df_existing.to_dict('records')
    else:
        scraped_urls = set()
        results = []

    valid_count = len(results)
    driver = setup_driver()
    queries = build_queries()
    
    try:
        for query in queries:
            print(f"Searching for: {query}")
            search_url = f"https://www.youtube.com/results?search_query={query}"
            driver.get(search_url)
            time.sleep(3)
            
            for _ in range(5):
                driver.execute_script("window.scrollBy(0, 3000);")
                time.sleep(2)
                
            soup = BeautifulSoup(driver.page_source, "html.parser")
            video_elements = soup.select("ytd-video-renderer")
            
            found_in_query = 0
            for element in video_elements:
                if valid_count >= TARGET_VIDEOS:
                    break
                    
                video_url_elem = element.select_one("a#video-title")
                if not video_url_elem:
                    continue
                    
                url = "https://www.youtube.com" + video_url_elem.get("href")
                if url in scraped_urls:
                    continue
                    
                if "/shorts/" in url:
                    continue

                print(f"[{valid_count+1}/{TARGET_VIDEOS}] Examining {url} ...")
                video_data = get_video_details(driver, url)
                
                views = video_data["Views"]
                upload_date = video_data["Upload_Date"]
                
                year = 0
                if upload_date and len(upload_date) >= 4:
                    try:
                        year = int(upload_date[:4])
                    except:
                        pass
                
                if views >= MIN_VIEWS and (MIN_YEAR <= year <= MAX_YEAR):
                    results.append(video_data)
                    scraped_urls.add(url)
                    valid_count += 1
                    print(f"  -> SUCCESS! Views: {views}, Year: {year}")
                    
                    # Safe progressive save
                    safe_save(results, EXCEL_FILE)
                else:
                    print(f"  -> Rejected. Views: {views}, Year: {year}")

            if valid_count >= TARGET_VIDEOS:
                break
                
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        if results:
            safe_save(results, EXCEL_FILE)
            print(f"Saved {len(results)} videos to {EXCEL_FILE}")

if __name__ == "__main__":
    main()
