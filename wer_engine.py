
import aptitude_tools as a


def expect_value_error(name, function):
    try:
        function()
    except ValueError as error:
        print(f"PASS: {name} -> {error}")
    except Exception as error:
        raise AssertionError(
            f"FAIL: {name} -> unexpected "
            f"{type(error).__name__}: {error}"
        ) from error
    else:
        raise AssertionError(
            f"FAIL: {name} -> ValueError was not raised"
        )


def run_tests():
    expect_value_error(
        "Empty average",
        lambda: a.calculate_average([])
    )

    expect_value_error(
        "Zero time",
        lambda: a.calculate_speed(120, 0)
    )

    expect_value_error(
        "Zero speed",
        lambda: a.calculate_time(120, 0)
    )

    expect_value_error(
        "Invalid numeric input",
        lambda: a.calculate_percentage("abc", 20)
    )

    print("\nAll aptitude tools error-handling tests passed!")


if __name__ == "__main__":
    run_tests()
