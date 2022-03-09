import sys

from persistence import _Repository, Supplier, Hat, Order

if __name__ == '__main__':
    args = sys.argv[1:]

    repo = _Repository(args[3])
    repo.create_tables()

    # parse config file
    config = open(args[0])
    config_lines = config.readlines()
    hats_num, suppliers_num = config_lines.pop(0).split(',')
    suppliers_num = suppliers_num[:len(suppliers_num) - 1]

    # create suppliers
    for i in range(0, int(suppliers_num)):
        id, name = config_lines[i + int(hats_num)].split(',')
        if str(name).endswith('\n'):
            name = name[:-1]
        repo.suppliers.insert(Supplier(id, name))

    # create hats
    for i in range(0, int(hats_num)):
        id, topping, supplier, quantity = config_lines[i].split(',')
        if str(quantity).endswith('\n'):
            quantity = quantity[:-1]
        repo.hats.insert(Hat(id, topping, supplier, quantity))

    config.close()

    # execute orders
    orders = open(args[1])
    orders_lines = orders.readlines()
    output = open(args[2], "x")
    for i in range(len(orders_lines)):
        location, topping = orders_lines[i].split(',')
        if str(topping).endswith('\n'):
            topping = topping[:-1]
        hat = repo.hats.order_next(topping)
        repo.orders.insert(Order(i + 1, location, hat.id))
        supplier = repo.suppliers.find(hat.supplier)
        output.write(hat.topping + ',' + supplier.name + ',' + location + '\n')

    repo.close()
    output.close()
    orders.close()
