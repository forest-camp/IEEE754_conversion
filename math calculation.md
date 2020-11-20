# math calculation

## IEEE754 floating representation

```python
     31
     |
     | 30    23 22                    0
     | |      | |                     |
-----+-+------+-+---------------------+
qnan 0 11111111 10000000000000000000000
snan 0 11111111 01000000000000000000000
+inf 0 11111111 00000000000000000000000
-inf 1 11111111 00000000000000000000000
+0   0 00000000 00000000000000000000000
-0   1 00000000 00000000000000000000000
-----+-+------+-+---------------------+
     | |      | |                     |
     | +------+ +---------------------+
     |    |               |
     |    v               v
     | exponent        fraction
     |
     v
     sign
```

```python
For normal number (exp != 0), mantissa is 24 bits with hidden 1, seems like I1F23.
For denorm number (exp == 0 and man != 0), mantissa is 24 bits with hidden 0.
Exponet of denorm number is -126.
```

## Calculate step overview

### Float mul

```python
step 0. Unpack numbers to sign, exponent, mantissa.
step 1. Mulinternel.
step 2. Normalize.
step 3. Pack sign, exponent, mantissa.
```

### Float add

```python
step 0. Unpack numbers to sign, exponent, mantissa.
step 1. Denormalize.
step 2. AddInternel.
step 3. Normalize.
step 4. Pack sign, exponent, mantissa.
```

## Implement

### AddInternel (n items, $n ≥ 2$)

```python
step 0. Unpack numbers to sign, exponent, mantissa. Then denormlize.
step 1. Find maximum exp.
step 2. All items align to maximum exp. (by right logical shift)
        {option}: keep_sticky, if shift bits larger than mantissa bits, keep 1 at ulp.
step 3. Mantissa addition as integer addition.
step 4. Normalize and pack.
```

### MulInternel (2 items)

```python
step 1. Exp addition.
step 2. Man multiplication.
step 3. Shift, left shift or right shift, control by padding and discard.
    discard_bits = 2 * kManBits > frac_bits ? 2 * kManBits - frac_bits : 0;
    padding_bits = 2 * kManBits < frac_bits ? frac_bits - 2 * kManBits : 0;
step 4. Normalize and pack.
```

### Normalize

```python
step 1. Mantissa align to man_bits.
step 2. Exponent calculate and mantissa shift.
```

### Denormalize

```python
Mainly do mantissa alignment if kKBits != in_frac_bits.
(because of addition guard bits always larger than 2 * in_frac_bits)
```

## Rounding modes

|mode     |interpretation                                        |
|:--      |:--                                                   |
|rn       |mantissa LSB rounds to nearest even                   |
|rna(rs)  |mantissa LSB rounds to nearest, ties away from zero   |
|rz       |mantissa LSB rounds towards zero                      |
|rm       |mantissa LSB rounds towards negative infinity         |
|rp       |mantissa LSB rounds towards positive infinity         |

## Operations and accuracy

### order of calculation

$A = 2^1 × 1.00000000000000000000001$
$B = 2^0 × 1.00000000000000000000001$
$C = 2^3 × 1.00000000000000000000001$
$( A + B ) + C = 2^3 × 1.01100000000000000000001011$
$A + ( B + C ) = 2^3 × 1.01100000000000000000001011$

`Mathematically, (A + B) + C does equal A + (B + C).`

$A + B = 2^1 × 1.1000000000000000000000110000...$
$rn(A + B) = 2^1 × 1.10000000000000000000010$
$B + C = 2^3 × 1.0010000000000000000000100100...$
$rn(B + C) = 2^3 × 1.00100000000000000000001$
$A + B + C = 2^3 × 1.0110000000000000000000101100...$
$rn(rn(A + B) + C) = 2^3 × 1.01100000000000000000010$
$rn(A + rn(B + C)) = 2^3 × 1.01100000000000000000001$

### precision between mul-add and fma

$a * b + c$

#### multiply, then add

```python
res = round(round(a * b) + c)
```

#### fused multiply-add(fma)

```python
res = round((a * b) + c)
```

#### some examples

##### first

$$x = 1.0008$$
$x^2 =  1.00160064$
$x^2 − 1 = 1.60064 × 10 ^{−4}$ `true value`
$rn(x^2 − 1) = 1.6006 × 10^{−4}$ `fused multiply-add`
$rn(x^2) = 1.0016 × 10^{−4}$
$rn(rn(x^2)−1) = 1.6000 × 10^{−4}$ `multiply, then add`

##### second

$A = 2^0 × 1.00000000000000000000001$
$B = −2^0 × 1.00000000000000000000010$
$rn(A × A + B) = 2^{−46} × 1.00000000000000000000000$
$rn(rn(A × A) + B) = 0$
