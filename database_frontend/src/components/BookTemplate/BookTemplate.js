import React, { useEffect, useState } from 'react';
import './BookTemplate.css';
import { NavLink } from 'react-router-dom';

const BookTemplate = ({onBookClicked2,index,title,cover,isbn,authors}) => {

    const [author_names,setAuthorNames] = useState('');

    useEffect(()=>{
        // for(let i=0; i<authors.length ;i++){
        //     setAuthorNames(author_names.concat(authors[i][0]))
        // }
        setAuthorNames(authors);
    },[])

    return(
        <div className='book_showcase'>
            <NavLink onClick={() => onBookClicked2(isbn)} to='/book'><img alt='' className='book_cover' src={`${cover}`} width='260px' height='420px'/></NavLink>
            <span className='book_title'>{`${title}`}</span>
            <span className='authors'>{`Authors: ${author_names}`}</span>
        </div>
    );
}

export default BookTemplate;