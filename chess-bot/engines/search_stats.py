class SearchStats:
    def __init__(self):
        self.reset()

    # Search
    def inc_depth(self):
        self._depth += 1

    # TT Hits
    def inc_hits_exact(self):
        self._hits_exact += 1

    def inc_hits_alpha(self):
        self._hits_alpha += 1

    def inc_hits_beta(self):
        self._hits_beta += 1

    def inc_hash_collision(self):
        self._inc_hash_collision += 1

    # Cut Offs
    def inc_alpha_cut_off(self):
        self._alpha_cut_off += 1

    def inc_beta_cut_off(self):
        self._beta_cut_off += 1

    def inc_stored_cut_off(self):
        self._stored_cut_off += 1

    # Checkmates detected
    def inc_checkmates_detected(self):
        self._checkmates_detected += 1

    # Nodes
    def inc_nodes_calculated(self):
        self._nodes_calculated += 1

    def inc_nodes_evaluated(self):
        self._nodes_evaluated += 1

    def inc_nodes_saved(self):
        self._nodes_saved += 1

    def reset(self):
        # Search
        self._depth = 1

        # Hits
        self._hits_exact = 0
        self._hits_alpha = 0
        self._hits_beta = 0
        self._inc_hash_collision = 0

        # Cut Offs
        self._alpha_cut_off = 0
        self._beta_cut_off = 0
        self._stored_cut_off = 0

        # Checkmates detected
        self._checkmates_detected = 0

        # Nodes
        self._nodes_calculated = 0
        self._nodes_evaluated = 0
        self._nodes_saved = 0

    def __str__(self):
        total_hits = self._hits_exact + self._hits_alpha + self._hits_beta
        total_cut_offs = self._alpha_cut_off + self._beta_cut_off + self._stored_cut_off
        return f"Depth: {self._depth}, Nodes calculated: {self._nodes_calculated} (evaluated: {self._nodes_evaluated}, saved:{self._nodes_saved}), Cut Offs: {total_cut_offs} (A:{self._alpha_cut_off}, B:{self._beta_cut_off}, S:{self._stored_cut_off}), Hits: {total_hits} (E:{self._hits_exact}, A:{self._hits_alpha}, B:{self._hits_beta}, Collisions:{self._inc_hash_collision}), Checkmates detected: {self._checkmates_detected}"
