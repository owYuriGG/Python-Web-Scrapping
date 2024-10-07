def selection_sort(games):
  for i in range(len(games)):
    menor_index = i
    for j in range(i+1, len(games)):
      if float(games[j]['preco']) < float(games[menor_index]['preco']):
        menor_index = j
    games[i], games[menor_index] = games[menor_index], games[i]

  return games