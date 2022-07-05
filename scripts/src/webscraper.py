from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
import time
import os
import re
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

start_dict = {
    0: [220, [12306, 12351, 12417], '19-20'],
    # 1: [202, [11551, 11717, 11780], '18-19'],
    # 2: [184, [10708, 10753, 10798], '17-18'],
    # 3: [165, [9872, 9917, 9962], '16-17'],
    # 4: [145, [9025, 9070, 9116], '15-16'],
    # 5: [127, [8149, 8194, 8239], '14-15'],
    # 6: [118, [7618, 7729], '13-14'],
    # 7: [109, [7066, 7111, 7177], '12-13']
}

leagues = {
  0: "nb1",
  1: "nb1bchar",
  2: "nb1bmar",
  #3: "nb2aszt",
  #4: "nb2bar",
  #5: "nb2bre",
  #6: "nb2erk",
  #7: "nb2sze",
  #8: "nb2toth"
}

for year in range (0, len(start_dict)):
    current_league = start_dict[year][0]
    start_game_list = start_dict[year][1]
    season = start_dict[year][2]

    for league_index in range(0, len(leagues)):

        league = leagues[league_index]

        print("league: ", league)
        league_link = 'http://chess.hu/csapatbajnoksagok/?b=' + str(current_league+league_index)

        driver.get(league_link)
        time.sleep(2)
        html = (driver.page_source)              #.encode('utf8', 'ignore')

        soup = BeautifulSoup(html, 'lxml')
        table = soup.find('table', {'id' : 'csapat_eredmenyek'})
        teams = table.find_all('a')

        for t in teams :
            print(t.get_text())

        # for team_link in table.find_all('a', href=True):
            # driver.get("http://chess.hu"+team_link['href'])
            # time.sleep(2)
            # html = (driver.page_source)      #.encode('ascii', 'ignore')
            # soup = BeautifulSoup(html, 'lxml')
            # player_list = soup.find('table', {'id' : 'erosorrend'})
            # teamName = soup.find('h5', {'id' : 'csRovidnev'}).text
            # output_rows = []
            # for table_row in player_list.findAll('tr'):
                # columns = table_row.findAll('td')
                # # print(columns)

                # output_row = []
                # for column in columns:
                    # output_row.append(column.text);

                # if len(columns) >= 6 :
                    # player_link = columns[1].find('a').get('href')
                    # player_ref = "http://chess.hu"+player_link
                    # driver.get(player_ref)
                    # time.sleep(1)
                    # html = (driver.page_source)      #.encode('ascii', 'ignore')
                    # s = BeautifulSoup(html, 'lxml')
                    # b_year = s.find('span', {'id':'szuletesiEv'}).text
                    # output_row.append(b_year)
                    # output_row.append(teamName)


                    # fide_id = s.find('span', {'id' : 'fide_id'}).text
                    # if fide_id == "" :
                        # output_rows.append(output_row)
                        # continue
                    # fide_link = "https://ratings.fide.com/profile/"+str(fide_id)
                    # print(fide_link)
                    # driver.get(fide_link+"/chart")
                    # time.sleep(3)

                    # html = (driver.page_source)      #.encode('ascii', 'ignore')
                    # fs = BeautifulSoup(html, 'lxml')

                    # std_elo = re.sub("\D", "", fs.find('div', {'class' : 'profile-top-rating-data profile-top-rating-data_gray'}).text)

                    # rapid_elo = re.sub("\D", "", fs.find('div', {'class' : 'profile-top-rating-data profile-top-rating-data_red'}).text)

                    # blitz_elo = re.sub("\D", "", fs.find('div', {'class' : 'profile-top-rating-data profile-top-rating-data_blue'}).text)

                    # output_row.append(std_elo)
                    # output_row.append(rapid_elo)
                    # output_row.append(blitz_elo)

                    # print(std_elo, rapid_elo, blitz_elo)
                    # row_idx = 0


                    # for row in fs.find('table', {'class' : 'profile-table profile-table_chart-table'}).tbody.find_all('tr'):
                        # # we need these until 2015-Jan
                        # if row_idx == 73 :
                            # break
                        # else:

                            # if len(row.find_all('td')) > 2 :
                                # output_row.append(row.find_all('td')[2].text)
                            # else:
                                # output_row.append('-')

                            # if len(row.find_all('td')) > 4:
                                # output_row.append(row.find_all('td')[4].text)
                            # else:
                                # output_row.append('-')

                            # if len(row.find_all('td')) > 6:
                                # output_row.append(row.find_all('td')[6].text)
                            # else:
                                # output_row.append('-')




                            # row_idx += 1

                    # driver.get(fide_link+"/calculations")

                    # time.sleep(3)


                    # html = (driver.page_source)      #.encode('ascii', 'ignore')
                    # fs_calc = BeautifulSoup(html, 'lxml')


                    # row_idx = 0

                    # if fs_calc.find('table', {'class' : 'profile-table profile-table_colors'}) is not None:
                        # for row in fs_calc.find('table', {'class' : 'profile-table profile-table_colors'}).tbody.find_all('tr'):
                            # # we need these until 2015-Jan but current month is on top, so +3 needed
                            # if row_idx == 74 :
                                # break
                            # else:

                                # if len(row.find_all('td')) > 1 :
                                    # output_row.append(row.find_all('td')[1].text) #output_row.append(row.find_all('td')[2].text)
                                # else:
                                    # output_row.append('-')

                                # if len(row.find_all('td')) > 2:
                                    # output_row.append(row.find_all('td')[2].text) #output_row.append(row.find_all('td')[2].text)
                                # else:
                                    # output_row.append('-')

                                # if len(row.find_all('td')) > 3:
                                    # output_row.append(row.find_all('td')[3].text) #output_row.append(row.find_all('td')[2].text)
                                # else:
                                    # output_row.append('-')

                                # #output_row.append(row.find_all('td')[2].text)#output_row.append(row.find_all('td')[4].text)
                                # #output_row.append(row.find_all('td')[3].text) #output_row.append(row.find_all('td')[3].text)

                                # row_idx += 1
                    # else:
                        # output_row.append('NA') #output_row.append(row.find_all('td')[2].text)
                        # output_row.append('NA')#output_row.append(row.find_all('td')[4].text)
                        # output_row.append('NA') #output_row.append(row.find_all('td')[3].text)

                        # row_idx += 1



                    # #print(player_ref + '  ' + age)


                    # #print(column.text)

                # #print(output_row)

                # output_rows.append(output_row)

            # #team_name = soup.find('h5', {'id': 'csRovidnev'}).text   #.encode('utf8');

            # dirname = season+league+'.csv'

            # with open(dirname, 'a', encoding="utf8") as csvfile:
                # writer = csv.writer(csvfile)
                # writer.writerows(output_rows)

            #--------------------------------------------- comment out: ctrl+Q

        spans = soup.find_all('span', {'class':'relativizer'})
        round_no = len(spans)
        pairs_in_one_rounds = int((round_no + 1) / 2)
        span_idx = 0
        current_pairing = start_game_list[league_index]
        for span in spans:
            link = span.find('a', href=True)
            for pair in range(0, pairs_in_one_rounds):
                output_rows = []

                goto_link = "http://chess.hu"+link['href']+"&mid="+str(current_pairing)

                driver.get(goto_link)

                time.sleep(2)
                html = (driver.page_source)    ##.encode('utf8', 'ignore')
                soup = BeautifulSoup(html, 'lxml')

                league_name = soup.find('span', {'class': 'bajnoksag_nev'})

                current_round = soup.find('h5', {'class': 'ford_title'})

                print(f'{goto_link}, {league_name.text}, {current_round.text}')

                header = soup.find('div', {'id': 'parti_box'}).find('h4')

                tr = soup.find('tr', {'class': 'kivalasztott'})
                current_pairing += 1
                if tr is not None:
                    td_list = tr.find_all("td")
                    location = td_list[-3].text
                    date = td_list[-2].text
                    referee = td_list[-1].text
                else:
                    break;
                start_time = soup.find('h4', {'class': 'ford_ido'}).text
                games = soup.find('table', {'id': 'partik'})

                home_team = soup.find('a', {'id': 'cs1head'}).text
                away_team = soup.find('a', {'id': 'cs2head'}).text

                board_num = 0
                for table_row in games.findAll('tr'):
                    columns = table_row.findAll('td')
                    output_row = []
                    for column in columns:
                        if column.find('span', {'class': 'badge white'})\
                                .find('span', {'class': 'kontumalt glyphicon glyphicon-plus'}):
                            output_row.append('+ -')
                        elif column.find('span', {'class': 'badge white'}) \
                                .find('span', {'class': 'kontumalt glyphicon glyphicon-minus'}):
                            output_row.append('- +')
                        else:
                            output_row.append(column.text)
                        #print(column.text)
                    if board_num % 2 == 1 :
                        output_row.insert(4, 'black')
                        output_row.insert(6, 'white')
                    else:
                        output_row.insert(4, 'white')
                        output_row.insert(6, 'black')
                    board_num += 1
                    output_row.extend([league, span_idx+1, season,
                                       start_time, date, referee,
                                       location])
                    output_row.insert(0, home_team)
                    output_row.insert(1, away_team)

                    output_rows.append(output_row)

                output_rows.pop(0)

                dirname = season+'.csv'

                with open(dirname, 'a', encoding="utf8") as csvfile:

                    writer = csv.writer(csvfile)
                    writer.writerows(output_rows)
                    print(output_rows)






                # #path = 'D:\\work\\sakkChampionship\\'+season



                # #print(dirname)
                # #if not os.path.exists(dirname):
                # #    os.makedirs(dirname)



            span_idx += 1

            #do smg





    # fordulo = 2193  #2194
    # parositas = 12305 #12306

    # for league_num in range(0,9):



        # fordulok_szama = 0
        # parositas_szama = 0

        # print(league_num)
        # league = leagues[league_num]
        # print(league)

        # if league_num == 1 or league_num ==2 or league_num ==4 or league_num ==6:
            # #print("igaz")
            # fordulok_szama = 11
            # parositas_szama = 6
        # else:
            # fordulok_szama = 9
            # parositas_szama = 5
        # print(fordulok_szama)
        # print(parositas_szama)
        # for i in range(0,fordulok_szama):
            # fordulo+=1
            # for j in range(0,parositas_szama):
                # parositas+=1
                # #print("ford: "+str(fordulo)+" game: " +str(parositas))
                # driver.get("http://chess.hu/merkozesek/?f="+str(fordulo)+"&mid="+str(parositas))
                # time.sleep(2)
                # html = (driver.page_source)    ##.encode('utf8', 'ignore')
                # soup = BeautifulSoup(html, 'lxml')


                # header = soup.find('div', {'id' : 'parti_box'}).find('h4')

                # tr = soup.find('tr', {'class' : 'kivalasztott'})
                # if tr is not None:
                    # td_list = tr.find_all("td")
                    # date = td_list[-2].text
                # else:
                    # break;
                # #print(date)

                # time = soup.find('h4', {'class' : 'ford_ido'}).text
                # #print(time)
                # partik = soup.find('table', {'id' : 'partik'})
                # #partik = soup.find('tbody')

                # output_rows = []
                # home_team = soup.find('a', {'id' : 'cs1head'}).text
                # #print(home_team)
                # away_team = soup.find('a', {'id' : 'cs2head'}).text
                # #print(away_team)
                # #print(home_team, away_team)

                # board_num = 0 ;
                # for table_row in partik.findAll('tr'):
                    # columns = table_row.findAll('td')
                    # output_row = []
                    # for column in columns:
                        # output_row.append(column.text)
                        # #print(column.text)
                    # if(board_num % 2 == 1 ):
                        # output_row.insert(4,'black')
                        # output_row.insert(6,'white')
                    # else:
                        # output_row.insert(4,'white')
                        # output_row.insert(6,'black')
                    # board_num+=1;
                    # output_row.insert(0,home_team)
                    # output_row.insert(1,away_team)
                    # output_row.append(time)
                    # output_row.append(date)
                    # output_row.append(league)


                    # output_rows.append(output_row)

                # output_rows.pop(0);


                # dirname = 'fordulo'+str(i+1)+league+'.csv'

                # #print(dirname)
                # #if not os.path.exists(dirname):
                # #    os.makedirs(dirname)

                # with open(dirname, 'a', encoding="utf8") as csvfile:

                    # writer = csv.writer(csvfile)
                    # writer.writerows(output_rows)


driver.quit()

#print(soup)
