function AttractionCard({
  image,
  name,
  description,
  time,
  rating,
  category,
  price,
  duration,
}) {
  return (
    <div className="attraction-card">

      {image && (
        <img
          src={image}
          alt={name}
          className="attraction-image"
        />
      )}

      <div className="attraction-card-content">

        {time && (
          <p className="attraction-time">
            {time}
          </p>
        )}

        <h3>
          {name}
        </h3>

        {description && (
          <p>
            {description}
          </p>
        )}

        {rating && (
          <p className="attraction-rating">
            ⭐ {rating}
          </p>
        )}

        {category && (
          <p className="attraction-category">
            🏛️ {category}
          </p>
        )}

        {(price || duration) && (
          <div className="attraction-details">

            {price && (
              <span>
                {price}
              </span>
            )}

            {duration && (
              <span>
                {duration}
              </span>
            )}

          </div>
        )}

        {!time && (
          <button className="explore-btn">
            Explore
          </button>
        )}

      </div>
    </div>
  );
}


export default AttractionCard;