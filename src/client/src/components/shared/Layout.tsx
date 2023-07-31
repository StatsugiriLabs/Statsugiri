import { FunctionComponent, ReactNode } from "react";
import Meta from "./Meta";
import Footer from "./Footer";
import NavBar from "./NavBar";

type Props = {
    children?: ReactNode;
};

const Layout: FunctionComponent<Props> = (props) => {
    return (
        <div>
            <Meta />
            <NavBar />
            <div className="container mx-auto flex justify-center">
                <main>
                    {props.children}
                    <Footer />
                </main>
            </div>
        </div>
    );
};

export default Layout;
