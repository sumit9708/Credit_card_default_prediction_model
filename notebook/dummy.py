 module_1:
    class: RandomForestClassifier
    module: sklearn.ensemble
    params:
      min_samples_leaf: 3
    search_param_grid:
      min_samples_leaf:
      - 3
      - 6

  module_2:
    class: GradientBoostingClassifier
    module: sklearn.ensemble
    params:
      min_samples_leaf: 3
    search_param_grid:
      min_samples_leaf:
      - 3
      - 6

  module_3:
    class: SVC
    module: sklearn.svm
    params:
      degree : 3
      kernel : 'rbf'
      gamma  : 'scale'
    search_param_grid:
      degree:
      - 3
      - 6
      kernel :
      - 'rbf'
      gamma :
      - 'scale'

  module_4:
    class: DecisionTreeClassifier
    module: sklearn.tree
    params:
      criterion : 'entropy'
      max_depth : 2
    search_param_grid:
      criterion:
      - 'entropy'
      - 'gini'
      max_depth:
      - 2
