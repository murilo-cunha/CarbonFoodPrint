import pandas as pd


def read_data(filename):
    df = pd.read_csv(filename, index_col=0)
    return df


def get_countries():
    df = read_data("df/CO2_per_country_ageGroup.csv")
    countries = list(df.index.unique())
    return get_dictionary_for_dash(countries)


def get_all_age_groups():
    df = read_data("df/CleanFoodData.csv")
    ageGroups = list(df['Pop_Class'].unique())
    return get_dictionary_for_dash(ageGroups)


def get_age_groups(country):
    df = read_data("df/CO2_per_country_ageGroup.csv")
    age_groups = list(df.loc[country].ageGroup.unique())
    return get_dictionary_for_dash(age_groups)


def get_food_categories():
    df = read_data("df/CO2Footprint.csv")
    return list(df['Category'].unique())


def get_food_items(country, age_group, category):
    df = read_data("df/CleanFoodData.csv")
    df2 = pd.read_csv("df/CO2Footprint.csv")
    food_items = list(df[(df.index == country) & (df['Pop_Class'] == age_group)].FoodId.unique())
    food_items_co2dataset = df2.loc[df2.index.isin(food_items)]
    food_items_by_category = list(food_items_co2dataset[food_items_co2dataset['Category'] == category].Food)
    return get_dictionary_for_dash(food_items_by_category)


def get_food_items_only_per_category(category):
    df2 = pd.read_csv("df/CO2Footprint.csv")
    return list(df2[df2['Category'] == category].Food)


def get_dictionary_for_dash(series):
    return [{'label': item, 'value': item} for item in series]


def get_slider_box_keys():
    keys = []
    categories = get_food_categories()
    for category in categories:
        subList = get_food_items_only_per_category(category)
        structuredSubList = ['slider-'+category+'-'+foodItem for foodItem in subList]
        keys = keys + structuredSubList
    return keys


def get_food_category_and_item_dictionary():
    newDict = {}
    food_categories = get_food_categories()
    for category in food_categories:
        newDict[category] = get_food_items_only_per_category(category)
    return newDict


def generate_data_arrays(consumption_dict):
    df = read_data("df/CO2Footprint.csv")
    data_arrays = {
        'your_food_choices_categories':[],
        'your_food_choices_item':[],
        'your_food_choices_emissions':[],
        'your_food_choices_all_categories': list(consumption_dict.keys()),
        'your_food_choices_aggregated_emissions':[0]*len(consumption_dict.keys())
    }
    for category in consumption_dict.keys():
        for item in consumption_dict[category].keys():
            if consumption_dict[category][item] != 0:
                food_item = df[df['Food']==item]
                emission =  consumption_dict[category][item]*list(food_item['Grams.CO2e.per.Serving'])[0]
                data_arrays['your_food_choices_categories'].append(category)
                data_arrays['your_food_choices_item'].append(item)
                data_arrays['your_food_choices_emissions'].append(emission)
                data_arrays['your_food_choices_aggregated_emissions'][data_arrays['your_food_choices_all_categories'].index(category)] += emission
    return data_arrays

def generate_data_arrays_country(country,age_group,your_total):
    df = pd.read_csv("df/CO2_per_country_ageGroup.csv")
    df = df[df['ageGroup']==age_group]
    df['Mean_CO2.g'] = df['Mean_CO2.g'].apply(lambda x: x*7)
    df2 = pd.DataFrame([['YOU','',your_total]],columns=['Country','ageGroup','Mean_CO2.g'])
    df = df.append(df2)
    df = df.sort_values(by=['Mean_CO2.g'])

    countryList = list(df['Country'])
    i = countryList.index('YOU')

    a = ['#8EB640']*len(list(df['Mean_CO2.g']))
    a[i]='rgba(1,1,1,1)'

    data_arrays = {
         'country':countryList,
         'country_emissions':list(df['Mean_CO2.g']),
         'color':a
    }
    return data_arrays

def calculate_my_carbon_food_print(consumption_dict):
    df = read_data("df/CO2Footprint.csv")
    my_carbon_food_print = 0
    for category in consumption_dict.keys():
        for item in consumption_dict[category].keys():
            if consumption_dict[category][item] != 0:
                food_item = df[df['Food'] == item]
                my_carbon_food_print += consumption_dict[category][item]*list(food_item['Grams.CO2e.per.Serving'])[0]
    return my_carbon_food_print


def get_carbon_food_print_for_country(country, age_group):
    df = read_data("df/CO2_per_country_ageGroup.csv")
    return int(df[(df.index == country) & (df['ageGroup'] == age_group)]['Mean_CO2.g'] * 7)
