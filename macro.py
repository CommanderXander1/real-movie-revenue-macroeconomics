from bs4 import BeautifulSoup as bs
import requests


def getCpiDict() -> dict:
    CPI_LINK = "https://www.minneapolisfed.org/about-us/monetary-policy/inflation-calculator/consumer-price-index-1913-"
    CPI = requests.get(CPI_LINK).text
    pCPI = bs(CPI, 'html.parser')

    table = pCPI.find(class_="i9-e-table__container i9-e-table__container--light")
    # print(table)

    cpiData = []
    cpiByYear = {}

    # add data to list
    for d in table.find_all('td'):
        cpiData.append(d.find('div').text.replace('\xa0', ''))

    for i in range(0, len(cpiData), 3):
        cpiByYear[cpiData[i]] = cpiData[i+1]
    return cpiByYear


def getMovieDict(offset=0) -> dict:
    MOVIES_LINK = f"https://www.boxofficemojo.com/chart/top_lifetime_gross/?area=XWW&offset={offset*200}"
    mData = bs(requests.get(MOVIES_LINK).text, 'html.parser')
    table = mData.find(class_="a-bordered a-horizontal-stripes a-size-base a-span12 mojo-body-table mojo-table-annotated")

    movieDataList = []
    movieByName = {}

    for d in table.find_all('td'):
        movieDataList.append(d.text.replace('\xa0', ''))


    for i in range(1, len(movieDataList), 4):
        movieByName[movieDataList[i]] = [movieDataList[i + 2], movieDataList[i + 1]]

    return movieByName


def getTopMoviesDict(cpi_dict, movie_dict) -> dict: 
    real_value_dict = {}
    temp = {}
    for l in movie_dict:
        for k, v in l.items():
            y1price = float(v[1].replace('$', '').replace(',',''))
            y1cpi = float(cpi_dict[v[0]].replace('$', '').replace(',',''))
            y2cpi = float(cpi_dict['2025'].replace('$', '').replace(',',''))
            temp[k] = y1price*(y2cpi/y1cpi)
        
    temp = sorted(temp.items(), key=lambda item: item[1], reverse=True)
    for d in temp:
        real_value_dict[d[0]] = d[1]
    return real_value_dict    # year 1 price * year 2 cpi/year 1 cpi


def top_movies(pages=1, display=25) -> None:
    movieDictList = [getMovieDict(i) for i in range(0, pages)]
    top = list(getTopMoviesDict(getCpiDict(), movieDictList).items())[0:display]
    for i in range(0, len(top)):
        print(f"{i + 1}. {top[i][0]}: ${int(top[i][1]):,}")


if __name__ == '__main__':
    top_movies(pages=10, display=30)
