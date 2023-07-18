import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import { FunctionComponent } from "react";

type Props = {
    snapshotDate: string;
};

const PsTeamsDateDropdown: FunctionComponent<Props> = ({ snapshotDate }) => {
    return (
        <div>
            <FormControl size="small" disabled>
                <label className="font-light text-sm mb-1 text-zinc-700">
                    Current Date
                </label>
                <Select
                    labelId="ps-teams-date-dropdown-label"
                    value={snapshotDate.toString()}
                    className="min-w-[300px] sm:min-w-[560px] md:min-w-[570px] xl:min-w-[340px]"
                >
                    <MenuItem value={snapshotDate.toString()}>
                        <strong>{snapshotDate.toString()}</strong>
                    </MenuItem>
                </Select>
            </FormControl>
        </div>
    );
};

export default PsTeamsDateDropdown;
