import pandas as pd
import os
import datetime

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"MindBoxTest")

def most_popular_product_per_lmonth(orders, order_lines):
    # что означает популярные продукты?
    # топ 3 продуктов? топ 5? я сделаю топ 1 (но если их несколько, то будет несколько)
    # если надо исправить, пишите
    today = datetime.datetime.today()
    orders["DateTime"]=pd.to_datetime(orders["DateTime"])
    monthly_orders = orders[(orders['DateTime'].dt.year == today.year) & (orders['DateTime'].dt.month == today.month)]
    monthly_order_lines=pd.DataFrame()
    for i in monthly_orders["OrderId"]:
        _order_lines = order_lines[order_lines["OrderId"]==i]
        monthly_order_lines=monthly_order_lines.append(_order_lines)
    return(monthly_order_lines["ProductId"].mode())

def total_sum_per_pop_product(ids,order_lines):
    sums=[]
    orders=[]
    for i in ids:
        product_lines = order_lines[order_lines["ProductId"] == i]
        orders.append(product_lines["OrderId"])
        sums.append(product_lines["Price"].sum())
    return(sums,orders)

def culc_average_sum_of_orders(ids,order_lines,orders):
    sums=[]
    corr_order_lines=pd.DataFrame()
    for i in orders:
        s = i.unique().size
        for j in i:
            corr_order_lines = corr_order_lines.append(order_lines[order_lines["OrderId"]==j])
        sums.append(corr_order_lines["Price"].sum()/s)
        # product_lines = order_lines[order_lines["ProductId"] == i]
    return(sums)

def main(orders_path_to_file,order_lines_path_to_file):

    orders=pd.read_csv(orders_path_to_file)
    order_lines=pd.read_csv(order_lines_path_to_file)

    pop_pr_ids=most_popular_product_per_lmonth(orders,order_lines)
    report=pd.DataFrame(data={"PopularProducts":pop_pr_ids})
    sum_per_product,corr_orders=total_sum_per_pop_product(pop_pr_ids,order_lines)
    report["SumProfit"]=sum_per_product
    asmpo=culc_average_sum_of_orders(pop_pr_ids,order_lines,corr_orders)
    return report

main(BASE_DIR+"/data/orders.csv", BASE_DIR + "/data/order_lines.csv")