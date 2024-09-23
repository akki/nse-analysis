"""
Miscellaneous Utility functions
"""

def get_xirr(investments: list[tuple[float, int]], current_value: float) -> float:
    """
    I have not looked too much into the "official" or "technical" definition of XIRR.
    All this is trying to do is - calculating the yearly rate at which the investment changed
        assuming a constant rate in the whole duration.
    Assumes 365 days in a year.

    Input:
        investments: A list of 2-tuple of (investment_value, days_ago)
        current_value: The value of the `investments` now after the `days_ago` time has passed
        Example - `investments=[(1000, 730), (1000, 365)], current_value=6000` -> means that
            a total of 2 investments were made.
            An amount of 1000 INR was invested 730 days (2 years) ago and
            another 1000 INR were invested 365 days (1 year) ago.
            The total corpus has now become 6000 INR. Out of this 6000 INR, 2000 INR were invested,
                remaining 4000 INR was profit.
            For this case, the XIRR 100% (the first investment has now become 4000 INR, while the 
                second one has become 2000 INR => total = 4000 + 2000 = 6000).
            So this function would return 100.
            Because [(1000 * (1 + X/100) ^ (730 / 365)) + (1000 * (1 + X/100) ^ (365 / 365))] = 6000,
                would provide X=100

    Returns a float number `X`, which means the investment changed at X% (yearly compounding rate).
    """
    total_investment = sum(investment for investment, _ in investments)
    if (total_investment == 0) or (total_investment == current_value):
        return 0.0  # Avoid division by zero

    # Function to calculate the total future value given a rate
    def future_value(rate):
        return sum(investment * (1 + rate / 100) ** (days / 365) for investment, days in investments)

    # Initialize variables for the iterative method
    xirr_guess = 0.1  # Initial guess for XIRR (10%)
    tolerance = 1e-6
    max_iterations = 1000

    for _ in range(max_iterations):
        fv = future_value(xirr_guess)
        if abs(fv - current_value) < tolerance:
            break
        
        # Calculate the derivative (slope) of the future value for the current guess
        derivative = sum(
            investment * (days / 365) * (1 + xirr_guess / 100) ** ((days / 365) - 1)
            for investment, days in investments
        )

        if derivative == 0:
            break  # Avoid division by zero

        # Update the guess using Newton's method
        xirr_guess -= (fv - current_value) / derivative

    return xirr_guess  # Return the annualized rate as a percentage
