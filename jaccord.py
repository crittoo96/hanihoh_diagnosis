from util import close_connection
from util import create_connection
from collections import defaultdict

messages = {}
nested_dict = lambda: defaultdict(nested_dict)
jaccord_map = nested_dict()

# ソースコード引用
# https://mieruca-ai.com/ai/jaccard_dice_simpson/

# 集合Aと集合Bのjaccord係数を算出する
# return float
def calc_jaccord(list_a, list_b):
    #集合Aと集合Bの積集合(set型)を作成
    set_intersection = set.intersection(set(list_a), set(list_b))
    #集合Aと集合Bの積集合の要素数を取得
    num_intersection = len(set_intersection)
 
    #集合Aと集合Bの和集合(set型)を作成
    set_union = set.union(set(list_a), set(list_b))
    #集合Aと集合Bの和集合の要素数を取得
    num_union = len(set_union)
 
    #積集合の要素数を和集合の要素数で割って
    #Jaccard係数を算出
    try:
        return float(num_intersection) / num_union
    except ZeroDivisionError:
        return 'infinity'

def calc():
    conn = create_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT p1.message,(SELECT count(*) FROM post p2 where p2.diagnosis = p1.diagnosis AND p2.message = p1.message) as cnt, (SELECT group_concat(t.name separator ',') FROM (SELECT post_meta2.name AS name, COUNT(*) as cnt2 FROM post p3 INNER JOIN post_meta post_meta2 ON p3.id = post_meta2.post_id WHERE p3.message = p1.message GROUP BY post_meta2.name ORDER BY cnt2 DESC ) AS t ) AS features FROM post p1 INNER JOIN post_meta on post_meta.post_id = p1.id WHERE p1.diagnosis = '性格' GROUP BY p1.message ORDER BY cnt DESC")
        res = cursor.fetchall()
        # r = res.fetchall()
        for rs in res:
            messages[rs['message']] = rs['features'].split(',')
    
    close_connection(conn)
    # print(messages)s

    for i, i_val in messages.items():
        for j, j_val in messages.items():
            if not jaccord_map[i][j] or not jaccord_map[j][i]:
                jaccord_map[i][j] = calc_jaccord(i_val, j_val)
                # print('dd')


if __name__ == '__main__':
    calc()
    csv = []
    total_val = 0.0
    for i, i_val in jaccord_map.items():
        row = []
        for j, j_val in i_val.items():
            print(i, j, j_val)
            if j_val == 1.0 or j_val == 0.0 or j_val < 0.25:
                j_val = 'infinity'
            else:
                total_val = total_val + j_val
            row.append(j_val)
        csv.append(row)
    # print(jaccord_map)
    print(csv)
    for i, i_val in jaccord_map.items():
        print(i)
    
    print(total_val / (66* 66 - 66) * 100)
    
