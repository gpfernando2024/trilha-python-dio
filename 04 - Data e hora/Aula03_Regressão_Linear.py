from sklearn.linear_model import Lasso, Ridge, ElasticNet
from sklearn.metrics import mean_squared_error, r2_score

# Gerando os dados
X = [[0, 0], [1, 1], [2, 2]]
Y = [0, 1, 2]

# Dividindo os dados em treino e teste (opcional)
# Como não há muitos dados, podemos usar o próprio X para treino e teste
X_train, X_test, Y_train, Y_test = X, X, Y, Y

# Lasso - criação da Regressão Lasso com parâmetro alpha (equivalente ao lambda)
lasso = Lasso(alpha=0.1)
lasso.fit(X_train, Y_train)
y_pred_lasso = lasso.predict(X_test)
r2_score_lasso = r2_score(Y_test, y_pred_lasso)

# Ridge
ridge = Ridge(alpha=0.1)
ridge.fit(X_train, Y_train)
y_pred_ridge = ridge.predict(X_test)
r2_score_ridge = r2_score(Y_test, y_pred_ridge)

# ElasticNet
enet = ElasticNet(alpha=0.1, l1_ratio=0.7)  # Corrigido o erro de digitação
enet.fit(X_train, Y_train)
y_pred_enet = enet.predict(X_test)
r2_score_enet = r2_score(Y_test, y_pred_enet)

# Impressão dos resultados
print(f"r^2 enet : {r2_score_enet:.6f}")
print(f"r^2 lasso : {r2_score_lasso:.6f}")
print(f"r^2 ridge : {r2_score_ridge:.6f}")
