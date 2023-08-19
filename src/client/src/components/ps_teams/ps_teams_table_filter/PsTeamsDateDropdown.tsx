import FormControl from "@mui/material/FormControl";
import TextField from "@mui/material/TextField";
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
                {/* TODO: Uncomment when date selection is implemented */}
                {/* <Select
                    labelId="ps-teams-date-dropdown-label"
                    value={snapshotDate.toString()}
                    className="min-w-[300px] sm:min-w-[560px] md:min-w-[570px] xl:min-w-[340px]"
                >
                    <MenuItem value={snapshotDate.toString()}>
                        <strong>{snapshotDate.toString()}</strong>
                    </MenuItem>
                </Select> */}
                <TextField
                    disabled
                    className="min-w-[300px] sm:min-w-[560px] md:min-w-[570px] xl:min-w-[340px]"
                    variant="standard"
                    value={snapshotDate.toString()}
                />
            </FormControl>
        </div>
    );
};

export default PsTeamsDateDropdown;
