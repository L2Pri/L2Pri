import xgboost as xgb

def get_data(file_loc):
    f = open(file_loc, 'r')
    data = []
    for line in f:
        new_arr = []
        arr = line.split(' #')[0].split()
        ''' Get the score and query id '''
        score = arr[0]
        q_id = arr[1].split(':')[1]
        new_arr.append(int(score))
        new_arr.append(int(q_id))
        arr = arr[2:]
        ''' Extract each feature from the feature vector '''
        for el in arr:
            new_arr.append(float(el.split(':')[1]))
        data.append(copy.deepcopy(new_arr))
    f.close()
    #print('length : %s'%len(data))
    return np.array(data)

def main():
    training_data = get_data('../data/cross_data_py/1/train.dat')
    test_data = get_data('../data/cross_data_py/1/test.dat')

    model = xgb.sklearn.XGBClassifier(
        nthread=20,
        learn_rate=0.1,
        max_depth=15,
        min_child_weight=2,
        subsample=0.8,
        colsample_bytree=1,
        objective='rank:pairwise',
        n_estimators=300,
        gamma=0,
        reg_alpha=0,
        reg_lambda=1,
        max_delta_step=0,
        scale_pos_weight=1
    )
    watchlist = [(X_train, y_train), (X_test, y_test)]
    model.fit(X_train, y_train, eval_set=watchlist, eval_metric='ndcg', early_stopping_rounds=10)
