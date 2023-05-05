import React,{ useEffect, useState } from 'react';
import Navigation from '../Navigation/Navigation';
import Header from '../Header/Header';
import Books from '../Books/Books';
import Book from '../Book/Book';
import { Routes, Route } from 'react-router-dom';
import UserInfo from '../UserInfo/UserInfo';
import Admin from '../AdminCompononent/Admin';



const Home = ({user, onRouteChange}) => {



    const [books,setBooks] = useState([]);
    const [borrowed,setBorrowed] = useState([]);
    const [requested,setRequested] = useState([]);
    const [activeBook, setActiveBook] = useState({});

    useEffect(() => {
        fetch('http://localhost:5000/books',{
            method: 'get',
            headers: {'Content-Type':'application/json'}
        })
        .then(response => response.json())
        .then(data => setBooks(data))

        fetch('http://localhost:5000/borrowed', {
            method: 'post',
            headers: {'Content-Type' : 'application/json'},
            body: JSON.stringify({
                role: user.role,
                school_name: user.school_name
            })
        })
        .then(response => response.json())
        .then(data => setBorrowed(data))

        fetch('http://localhost:5000/borrowed', {
            method: 'post',
            headers: {'Content-Type' : 'application/json'},
            body: JSON.stringify({
                role: user.role,
                school_name: user.school_name
            })
        })
        .then(response => response.json())
        .then(data => setRequested(data))

    }, [])
    

    const onBookClicked = (index) => {
        setActiveBook(books[index]);
    }

    return(
            <>
                <Navigation onRouteChange={onRouteChange}/>
                <Routes>
                    <Route path='/' element={
                        <div>
                            <Header first_name={user.first_name} last_name={user.last_name} school={user.school}/>
                            <Books books={books} onBookClicked={onBookClicked}/>
                        </div>
                    } />
                    <Route path="/book" element={
                        <Book user={user} book={activeBook}/>
                    } />
                    <Route path='/myProfile' element={
                        <UserInfo user={user}/>
                    }/>
                    <Route path='/borrowed' element={
                        user.role === 'admin'
                        ? <Admin book_list={borrowed} borrow={true} />
                        : <Books books={borrowed} onBookClicked={onBookClicked}/>
                    }/>
                    <Route path='/requested' element={
                        user.role === 'admin'
                        ? <Admin book_list={requested} borrow={false} />
                        : <Books books={requested} onBookClicked={onBookClicked}/>
                    }/>

                </Routes>
            </>
    );
}

export default Home;