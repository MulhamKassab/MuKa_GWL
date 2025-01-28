def calculate_lr(nfl_result, gtf, lsf_value, glazing_type):
    """
    Calculate the Load Resistance (LR) based on the NFL results, GTF values,
    Load Share Factor (LSF), and the type of glazing (single or double).

    Args:
        nfl_result (list or float): NFL results calculated from the NFL interpolation function.
                                    For double glazing, it should be a list of two values.
        gtf (dict): GTF (Glass Thickness Factor) values for short and long durations,
                    where gtf['short'] and gtf['long'] are lists of GTF values.
        lsf_value (dict): Load Share Factor values for double glazing. It should contain:
                          - 'short_duration': A list of two LSF values (one for each layer).
                          - 'long_duration': A list of two LSF values (one for each layer).
        glazing_type (str): The type of glazing ('single' or 'double').

    Returns:
        dict: A dictionary containing the calculated LR for 'short' and 'long' durations.
              For double glazing, each duration will have two LR values (one for each layer).
              For single glazing, each duration will have one LR value.
    """


    # Initialize a dictionary to store the final LR results
    lr_result = {}

    # Iterate through both 'short' and 'long' GTF durations
    for duration in gtf:
        gtf_duration = gtf[duration]

        # Ensure GTF values are converted to floats for mathematical operations
        gtf_duration = [float(g) for g in gtf_duration]

        # Handle double glazing calculations
        if glazing_type == "double":
            # Validate the structure of LSF values for double glazing
            if f'{duration}_duration' not in lsf_value or len(lsf_value[f'{duration}_duration']) != 2:
                raise ValueError(f"Invalid LSF structure for {duration} duration: {lsf_value}")

            # Extract LSF values for both layers
            lsf_ls1 = lsf_value[f'{duration}_duration'][0]
            lsf_ls2 = lsf_value[f'{duration}_duration'][1]

            # Validate that nfl_result contains exactly two values for double glazing
            if len(nfl_result) != 2:
                raise ValueError(f"Invalid nfl_result for double glazing: {nfl_result}")

            # Calculate LR for each layer
            lr1 = nfl_result[0] * gtf_duration[0] * lsf_ls1  # First layer
            lr2 = nfl_result[1] * gtf_duration[1] * lsf_ls2  # Second layer

            # Store the LR values for both layers in the result dictionary
            lr_result[duration] = [lr1, lr2]
        else:
            # For single glazing, multiply NFL result by GTF values
            lr_result[duration] = [nfl_result * g for g in gtf_duration]


    # Return the calculated LR results
    return lr_result
