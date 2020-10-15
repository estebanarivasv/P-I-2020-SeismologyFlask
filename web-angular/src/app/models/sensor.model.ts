import { UserModel } from './user.model'

export interface ISensor {
    // Properties
    id_num: number;
    name: string;
    ip: string;
    port: number;
    status: boolean;
    active: boolean;
    user_id?: number;
    user?: UserModel

    // Methods
}

export class SensorModel implements ISensor {
    constructor(
        public id_num: number,
        public name: string,
        public ip: string,
        public port: number,
        public status: boolean,
        public active: boolean,
        public user_id?: number,
        public user?: UserModel
    )
    // Constructor implementation
    {
        
    }
}