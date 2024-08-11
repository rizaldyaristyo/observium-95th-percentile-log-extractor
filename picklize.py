import pickle

ids=[
        [152, 'Store 1', 'ISP 1'],
        [46, 'Store 2', 'ISP 1'],
        [47, 'Store 2', 'ISP 2'],
        [235, 'HQ Office', 'ISP 1'],
        [238, 'HQ Office', 'ISP 2'],
        [426, 'HQ Pakis', 'ISP 2'],
        [427, 'HQ Pakis', 'ISP 3'],
        [202, 'Factory 1', 'ISP 2'],
        [138, 'HQ Tower', 'ISP 1'],
        [140, 'HQ Tower', 'ISP 2'],
        [139, 'HQ Tower', 'ISP 1'],
        [7, 'Guest Villa', 'ISP 3'],
        [8, 'Guest Villa', 'ISP 1'],
        [469, 'Factory Distribution', 'ISP 1'],
        [124, 'Factory Healthcare', 'ISP 1'],
        [27, 'Factory FNB', 'ISP 2'],
        [96, 'Factory District B', 'ISP 1'],
        [98, 'Factory District B', 'ISP 3'],
        [59, 'Factory Packing District B', 'ISP 2'],
        [69, 'Factory Packing District A', 'ISP 2'],
        [278, 'Salon', 'ISP 1'],
        [85, 'Beauty Clinic District C', 'ISP 2'],
        [89, 'Beauty Clinic District C', 'ISP 3'],
        [1, 'Beauty Clinic District D', 'ISP 3'],
    ]

with open('ids.pickle', 'wb') as file:
    pickle.dump(ids, file)
