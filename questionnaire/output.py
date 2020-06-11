import csv


def model_out_put(model):
    m = model.objects.all()
    data = [x.to_dict() for x in m]
    k_data = list([x.keys() for x in data][0])
    v_data = list(x.values() for x in data)

    with open(f'./アンケート/{model.title}.csv', "w", newline='') as f:
        output_writer = csv.writer(f)
        output_writer.writerow(k_data)
        for data_row in v_data:
            output_writer.writerow(data_row)
