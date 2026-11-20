function BudgetCard({
  totalBudget,
  planned,
  remaining,
  percentage,
  breakdown,
  overBudget
}) {

  const safeTotal =
    Number(totalBudget || 0);

  const safePlanned =
    Number(planned || 0);

  const safeRemaining =
    Number(remaining || 0);

  const safePercentage =
    Number(percentage || 0);


  return (
    <div className="budget-card">

      <h2>
        Trip Budget
      </h2>


      <div className="budget-row">

        <span>
          Total Budget
        </span>

        <strong>
          ₹{safeTotal.toLocaleString()}
        </strong>

      </div>


      <div className="budget-row">

        <span>
          Planned
        </span>

        <strong>
          ₹{safePlanned.toLocaleString()}
        </strong>

      </div>


      <div className="budget-row">

        <span>
          Remaining
        </span>

        <strong>
          ₹{safeRemaining.toLocaleString()}
        </strong>

      </div>


      <div className="budget-progress">

        <div
          className="budget-progress-fill"
          style={{
            width: `${Math.min(
              100,
              Math.max(
                0,
                safePercentage
              )
            )}%`
          }}
        />

      </div>


      <p className="budget-percentage">
        {safePercentage.toFixed(1)}% planned
      </p>


      {overBudget && (
        <p className="budget-warning">
          ⚠️ Trip is over budget.
        </p>
      )}


      {breakdown && (
        <div className="budget-breakdown">

          <h3>
            Breakdown
          </h3>

          <div className="budget-row">
            <span>
              Accommodation
            </span>
            <strong>
              ₹{Number(
                breakdown.accommodation || 0
              ).toLocaleString()}
            </strong>
          </div>

          <div className="budget-row">
            <span>
              Intercity Transportation
            </span>
            <strong>
              ₹{Number(
                breakdown.intercity_transportation || 0
              ).toLocaleString()}
            </strong>
          </div>

          <div className="budget-row">
            <span>
              Local Transportation
            </span>
            <strong>
              ₹{Number(
                breakdown.local_transportation || 0
              ).toLocaleString()}
            </strong>
          </div>

          <div className="budget-row">
            <span>
              Food
            </span>
            <strong>
              ₹{Number(
                breakdown.food || 0
              ).toLocaleString()}
            </strong>
          </div>

          <div className="budget-row">
            <span>
              Activities
            </span>
            <strong>
              ₹{Number(
                breakdown.activities || 0
              ).toLocaleString()}
            </strong>
          </div>

          <div className="budget-row">
            <span>
              Miscellaneous
            </span>
            <strong>
              ₹{Number(
                breakdown.miscellaneous || 0
              ).toLocaleString()}
            </strong>
          </div>

        </div>
      )}

    </div>
  );
}


export default BudgetCard;