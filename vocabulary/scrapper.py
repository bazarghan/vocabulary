from bs4 import BeautifulSoup
import cloudscraper

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3'
}


def get_page(url):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url, headers=headers)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        return None


def get_word(word):
    base_url = "https://vocabulary.com/"
    soup = get_page(f'{base_url}dictionary/{word}')
    word_soup = soup.find_all('div', class_='word-area')
    if not word_soup:
        return None

    original_word = word_soup[0].find('h1').text.strip()
    audios = soup.find_all('a', class_="audio")

    if len(audios) == 0:
        american_audio_url = None
        british_audio_url = None
    elif len(audios) == 1:
        british_audio_url = None
        american_audio_url = 'https://audio.vocabulary.com/1.0/us/' + audios[0].attrs['data-audio'] + '.mp3'
    else:
        american_audio_url = 'https://audio.vocabulary.com/1.0/us/' + audios[0].attrs['data-audio'] + '.mp3'
        if audios[1].find('audio') is not None:
            british_audio_url = audios[1].find('audio')['src']
        else:
            british_audio_url = None

    phonetics = soup.find_all('span', class_='span-replace-h3')
    if len(phonetics) == 0:
        american_phonetic = None
        british_phonetic = None
    elif len(phonetics) == 1:
        american_phonetic = phonetics[0].text.strip()
        british_phonetic = None
    else:
        american_phonetic = phonetics[0].text.strip()
        british_phonetic = phonetics[1].text.strip()

    short_def = soup.find('p', class_='short').text.strip()
    long_def = soup.find('p', class_='long').text.strip()

    lis = soup.find_all('li', class_='sense')
    defs = []
    for li in lis:
        part_of_speech = li.find('div', class_='pos-icon').text.strip()
        div = li.find('div', class_='definition')
        div.find('div', class_='pos-icon').decompose()
        definition = div.get_text(separator=' ', strip=True)
        defs.append((part_of_speech, definition))

    obj = {
        'original_word': original_word,
        'british_audio_url': british_audio_url,
        'american_audio_url': american_audio_url,
        'british_phonetic': british_phonetic,
        'american_phonetic': american_phonetic,
        'short_def': short_def,
        'long_def': long_def,
        'defs': defs
    }
    return obj
