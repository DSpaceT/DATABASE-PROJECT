import React,{useState,useEffect} from "react";
import Reviews from "../Reviews/Reviews";
import './Review_list.css';

const Review_list = ({user}) =>{

    const [reviews,setReviews] = useState([]);
    const [count2,setCount2] = useState(0);

    useEffect(()=>{
        fetchRevs();
    },[count2])

    const fetchRevs = async () =>{

        await fetch('http://localhost:5000/reviews', {
            method: 'post',
            headers: {
                'Content-Type' : 'application/json'
            },
            body: JSON.stringify({
                role: 'Admin',
                username: user.username
            })
        })
        .then(response => response.json())
        .then(data => {
            setReviews(data);
            console.log(data);
        })
    }

    const update_count = () =>{{
        setCount2(count2+1);
    }}

    const onApproveReview = async (approve,isbn,username) => {
        await fetch('http://localhost:5000/accept_review', {
            method: 'post',
            headers: {
                'Content-Type' : 'application/json'
            },
            body: JSON.stringify({
                isbn: isbn,
                username: username,
                approved: approve
            })
        })
        .then(response => response.json())
        .then(data => console.log(data))

        update_count();
    }

    return(
        <div>
            <div className='review_box2'> 
                    {
                        reviews.map((review,index) => {
                            return(
                                <div key={index} className="review_container2">
                                    <div>
                                        <Reviews className='review_to_approve' title={review.title} date={review.review_date} submited_by={review.first_name.concat(' ',review.last_name)} show_title={true} score={review.score} desc={review.description}/>
                                    </div>
                                    <button onClick={() => onApproveReview(1,review.isbn,review.username)}>Approve</button>
                                    <button onClick={() => onApproveReview(0,review.isbn,review.username)}>Reject</button>
                                </div>
                            );
                        })
                    }
                    </div>
        </div>
    )
}

export default Review_list;