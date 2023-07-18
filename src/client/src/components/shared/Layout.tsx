import { FunctionComponent, ReactNode } from "react";
import Meta from "./Meta";

type Props = {
    children?: ReactNode;
};

const Layout: FunctionComponent<Props> = (props) => {
    return (
        <div>
            <Meta />
            <p>Nav</p>
            <div className="container mx-auto flex justify-center">
                <main className={""}>
                    <p>Header</p>
                    {props.children}
                </main>
            </div>
        </div>
    );
};

export default Layout;
