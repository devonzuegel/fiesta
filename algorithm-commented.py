
initialize transl_prob(e|f) uniformly
do until convergence
  set count(e|f) to 0 for all e,f
  set total(f) to 0 for all f
  for all sentence pairs (e_s,f_s)
    set total_s(e) = 0 for all e
    for all words e in e_s
      for all words f in f_s
        total_s(e) += transl_prob(e|f)
    for all words e in e_s
      for all words f in f_s
        count(e|f) += transl_prob(e|f) / total_s(e)
        total(f)   += transl_prob(e|f) / total_s(e)
  for all f
    for all e
      transl_prob(e|f) = count(e|f) / total(f)
