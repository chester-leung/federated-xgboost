import sys
import xgboost as xgb 

rabit_config = sys.argv[1]

# Instantiate Federated XGBoost
root_cert = "certs/root_cert.crt"
cert_chain = "certs/cert_chain.crt"
private_key = "certs/private_key.pem"

fed = xgb.Federated(rabit_config, root_cert, cert_chain, private_key)

# Get number of federating parties
print("Number of parties in federation: ", fed.get_num_parties())

# Load training data
# Ensure that each party's data is in the same location with the same name
dtrain = fed.load_data("/home/ubuntu/federated-xgboost/demo/data/hb_train.csv")
dval = fed.load_data("/home/ubuntu/federated-xgboost/demo/data/hb_val.csv")

# Train a model
params = {
        "max_depth": 3, 
        "min_child_weight": 1.0, 
        "lambda": 1.0,
        "tree_method": "hist",
        "objective": "binary:logistic"
        }

num_rounds = 20
print("Training")
bst = xgb.train(params, dtrain, num_rounds, evals=[(dtrain, "dtrain"), (dval, "dval")])

dtest = fed.load_data("/home/ubuntu/federated-xgboost/demo/data/hb_test.csv")

# Get predictions
print("Predicting")
ypred = bst.predict(dtest)

print("The first twenty predictions are: ", ypred[:20])

# Save the model
bst.save_model("sample_model.model")

# Shutdown
fed.shutdown()
