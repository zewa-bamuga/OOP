import React from "react";
import logo from '../img/logo.png';
import banner from "../img/banner.png"

export default function Header() {
    return (
        <header>
            <div className="menu">
                <ul className="nav">
                    <li>сотрудники</li>
                    <li>направления</li>
                    <li>новости</li>
                </ul>
            </div>
            <div className="circle">
                <img src={logo} alt="Фотография" />
            </div>
            <div className='presentation'>
                <img src={banner} alt="Фотография"/>
            </div>
        </header>
    )
}
