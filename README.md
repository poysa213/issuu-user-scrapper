# Issuu user's PDF Downloader

A Python script that allows you to download PDF files from Issuu using web scraping techniques. The script utilizes the Issuu website and Selenium WebDriver to scrape document links from a given profile URL and download the corresponding PDF files. It uses multiprocessing for parallel downloading and provides a progress bar using tqdm.

## Description

Issuu is a digital publishing platform that allows users to upload and share PDF documents. This script automates the process of downloading PDF files from Issuu by extracting the document links and saving them locally.

The script is built with Python and uses the Selenium library for web scraping and browser automation. It leverages Chrome WebDriver to interact with the Issuu website, input the document URL, and initiate the PDF download. The script also utilizes the requests library to download the PDF files and the tqdm library to display a progress bar during the download process.

## Requirements

- Python 3.x
- Chrome web browser
- Selenium library
- Requests library
- Webdriver Manager library
- tqdm library

## Installation

1. Clone the repository:

```
git clone https://github.com/poysa213/issuu-user-scrapper.git
```

2. Install the required dependencies:

```
pip install selenium requests webdriver_manager tqdm
```
or 

```
pip install -r requirements.txt
```

3. Download and install the Chrome web browser if you haven't already.

## Usage

1. Run the script:

```
python main.py
```

2. When prompted, enter the profile URL from Issuu for which you want to download the PDF files.
```
https://issuu.com/username/docs/
```


3. Enter the path to the folder where you want to save the downloaded PDF files.
```
/home/username/pdfs
or
D:\pdfs
```


4. The script will scrape the document links from the profile page and initiate the download process. It will display a progress bar indicating the status of the downloads.

5. Once the script completes, you will find the downloaded PDF files in the specified folder.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
