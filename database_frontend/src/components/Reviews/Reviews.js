import React from "react";
import './Reviews.css'

const Reviews = ({score, submited_by, desc,show_title,title,show_desc, showCat, category}) =>{

    return(
        <div className="review">
            <div>
                {showCat
                    ?   <span>{`${category}`}</span>
                    :   <span>{`${submited_by}:`}</span>
                }
                <span>{`${score}`}</span>
                {
                    show_title
                    ?   <span>{`${title}`}</span>
                    :   <div></div>
                }
            </div>
            {
                show_desc
                ? <p>{`${desc}`}</p>
                : <div></div>
            }
        </div>
    );

}

export default Reviews;