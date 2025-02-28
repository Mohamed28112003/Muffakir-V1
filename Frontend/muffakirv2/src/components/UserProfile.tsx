import React from 'react';
import { PiStudentBold } from "react-icons/pi";

const UserProfile = ({guest} : {guest : string}) => {

  return (
    <div className='profile'>
        {guest}
        <PiStudentBold size={32} />
    </div>
  );
};

export default UserProfile;
