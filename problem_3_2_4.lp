\ COSC-364 Assignment 2 LP Generator, LP Output File
\ Written by Will Cowper (81163265), Jesse Sheehan (53366509)
\ Parameters: X=3, Y=2, Z=4, Split=2, Demand=2 * i + j


MINIMIZE
	r

SUBJECT TO

	\ DEMAND CONSTRAINTS
	x_111 + x_121 = 3
	x_112 + x_122 = 4
	x_113 + x_123 = 5
	x_114 + x_124 = 6
	x_211 + x_221 = 5
	x_212 + x_222 = 6
	x_213 + x_223 = 7
	x_214 + x_224 = 8
	x_311 + x_321 = 7
	x_312 + x_322 = 8
	x_313 + x_323 = 9
	x_314 + x_324 = 10

	\ CAPACITY CONSTRAINTS FOR LINKS BETWEEN SOURCE AND TRANSIT NODES
	x_111 + x_112 + x_113 + x_114 - c_11 = 0
	x_121 + x_122 + x_123 + x_124 - c_12 = 0
	x_211 + x_212 + x_213 + x_214 - c_21 = 0
	x_221 + x_222 + x_223 + x_224 - c_22 = 0
	x_311 + x_312 + x_313 + x_314 - c_31 = 0
	x_321 + x_322 + x_323 + x_324 - c_32 = 0

	\ CAPACITY CONSTRAINTS FOR LINKS BETWEEN TRANSIT AND DESTINATION NODES
	x_111 + x_211 + x_311 - d_11 = 0
	x_112 + x_212 + x_312 - d_12 = 0
	x_113 + x_213 + x_313 - d_13 = 0
	x_114 + x_214 + x_314 - d_14 = 0
	x_121 + x_221 + x_321 - d_21 = 0
	x_122 + x_222 + x_322 - d_22 = 0
	x_123 + x_223 + x_323 - d_23 = 0
	x_124 + x_224 + x_324 - d_24 = 0

	\ OBJECTIVE FUNCTION LOAD CONSTRAINTS
	c_11 + c_21 + c_31 - r <= 0
	c_12 + c_22 + c_32 - r <= 0
	c_13 + c_23 + c_33 - r <= 0
	c_14 + c_24 + c_34 - r <= 0

	\ TRANSIT NODE LOAD CONSTRAINTS
	x_111 + x_112 + x_113 + x_114 + x_211 + x_212 + x_213 + x_214 + x_311 + x_312 + x_313 + x_314 - l_1 = 0
	x_121 + x_122 + x_123 + x_124 + x_221 + x_222 + x_223 + x_224 + x_321 + x_322 + x_323 + x_324 - l_2 = 0

	\ BINARY VARIABLE AND DECISION VARIABLE CONSTRAINTS
	2 x_111 - 3 u_111 = 0
	2 x_112 - 4 u_112 = 0
	2 x_113 - 5 u_113 = 0
	2 x_114 - 6 u_114 = 0
	2 x_121 - 3 u_121 = 0
	2 x_122 - 4 u_122 = 0
	2 x_123 - 5 u_123 = 0
	2 x_124 - 6 u_124 = 0
	2 x_211 - 5 u_211 = 0
	2 x_212 - 6 u_212 = 0
	2 x_213 - 7 u_213 = 0
	2 x_214 - 8 u_214 = 0
	2 x_221 - 5 u_221 = 0
	2 x_222 - 6 u_222 = 0
	2 x_223 - 7 u_223 = 0
	2 x_224 - 8 u_224 = 0
	2 x_311 - 7 u_311 = 0
	2 x_312 - 8 u_312 = 0
	2 x_313 - 9 u_313 = 0
	2 x_314 - 10 u_314 = 0
	2 x_321 - 7 u_321 = 0
	2 x_322 - 8 u_322 = 0
	2 x_323 - 9 u_323 = 0
	2 x_324 - 10 u_324 = 0

	\ BINARY VARIABLE CONSTRAINTS (ONLY 2 ACTIVE TRANSIT NODES)
	u_111 + u_121 = 2
	u_112 + u_122 = 2
	u_113 + u_123 = 2
	u_114 + u_124 = 2
	u_211 + u_221 = 2
	u_212 + u_222 = 2
	u_213 + u_223 = 2
	u_214 + u_224 = 2
	u_311 + u_321 = 2
	u_312 + u_322 = 2
	u_313 + u_323 = 2
	u_314 + u_324 = 2

BOUNDS

	\ NON-NEGATIVITY CONSTRAINTS
	r >= 0
	x_111 >= 0
	x_112 >= 0
	x_113 >= 0
	x_114 >= 0
	x_121 >= 0
	x_122 >= 0
	x_123 >= 0
	x_124 >= 0
	x_211 >= 0
	x_212 >= 0
	x_213 >= 0
	x_214 >= 0
	x_221 >= 0
	x_222 >= 0
	x_223 >= 0
	x_224 >= 0
	x_311 >= 0
	x_312 >= 0
	x_313 >= 0
	x_314 >= 0
	x_321 >= 0
	x_322 >= 0
	x_323 >= 0
	x_324 >= 0
	c_11 >= 0
	c_12 >= 0
	c_21 >= 0
	c_22 >= 0
	c_31 >= 0
	c_32 >= 0
	d_11 >= 0
	d_12 >= 0
	d_13 >= 0
	d_14 >= 0
	d_21 >= 0
	d_22 >= 0
	d_23 >= 0
	d_24 >= 0

BIN

	\ BINARY VARIABLES
	u_111
	u_112
	u_113
	u_114
	u_121
	u_122
	u_123
	u_124
	u_211
	u_212
	u_213
	u_214
	u_221
	u_222
	u_223
	u_224
	u_311
	u_312
	u_313
	u_314
	u_321
	u_322
	u_323
	u_324

END
