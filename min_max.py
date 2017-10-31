def minmax(state, depth=2):

	def ft_max(state, alpha, beta, d):
		if state.is_terminal() or d >= depth:
			return state.heuristic_value
		node_value = float('-inf')
		for i, move in enumerate(state.available_moves):
			node_value = max(node_value, ft_min(state.next_state(move),alpha, beta, d+1))
			if node_value >= beta:
				return node_value
			alpha = max(alpha, node_value)
#			print("alpha", alpha)
		return node_value

	def ft_min(state, alpha, beta, d):
		if state.is_terminal() or d >= depth:
			return state.heuristic_value
		node_value = float('inf')
		for i, move in enumerate(state.available_moves):
			node_value = min(node_value, ft_max(state.next_state(move),alpha, beta, d+1))
			if node_value <= alpha:
				return node_value
			beta = min(beta, node_value)
#			print("beta", beta)
		return node_value

	alpha = float('-inf')
	beta = float('inf')
	node_value = float('-inf')
	next_move = state.available_moves[0]
	print(next_move)
	for i, move in enumerate(state.available_moves):
		neirval = ft_min(state.next_state(move), alpha, beta, 1)
		if neirval > node_value:
			node_value = neirval
			next_move = move
		alpha = max(alpha, node_value)
#	print(next_move)
	return next_move	
