
// First, we define the interface that lets us work with jsons from api
export interface IUser {
    // Properties
    id_num: number;
    email: string;
    admin: boolean;
    password?: string;  // OPTIONAL

    // Methods
}

export class UserModel implements IUser {
    constructor(
        public id_num: number,
        public email: string,
        public admin: boolean,
        public password?: string  // OPTIONAL
    )
    // Constructor implementation
    {

    }
}