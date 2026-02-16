def normalize_name(name: str):
    return sorted(name.lower().strip().split())


def evaluate_primary(customer, input_data):
    input_names = normalize_name(input_data["full_name"])
    stored_names = normalize_name(customer.full_name)

    if (
        input_names == stored_names
        and customer.id_number == input_data["id_number"]
        and customer.yob == input_data["yob"]
    ):
        return True

    return False
