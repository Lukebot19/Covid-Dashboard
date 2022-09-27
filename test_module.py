from covid_data_handler import covid_api_request, parse_csv_data , process_covid_csv_data, schedule_covid_updates



def test_parse_csv_data ():
    data = parse_csv_data ( 'nation_2021-10-28.csv' )
    assert len ( data ) == 639, 'Its broken'

def test_process_covid_csv_data ():
    last7days_cases , current_hospital_cases , total_deaths = process_covid_csv_data ( parse_csv_data ( 'nation_2021-10-28.csv' ) )
    assert last7days_cases == 240299, 'Its broken'
    assert current_hospital_cases == 7019, 'Its broken'
    assert total_deaths == 141544, 'Its broken'

test_parse_csv_data()
test_process_covid_csv_data()