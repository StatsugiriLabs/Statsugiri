import FormControl from "@mui/material/FormControl";
import MenuItem from "@mui/material/MenuItem";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import Router from "next/router";
import { FunctionComponent, useEffect, useRef, useState } from "react";
import { Format } from "../../../../types";

type Props = {
    format: string;
};

const PsTeamsFormatDropdown: FunctionComponent<Props> = ({ format }) => {
    const [selectedFormat, setSelectedFormat] = useState<String>(format);
    const firstUpdate = useRef(true);

    useEffect(() => {
        if (firstUpdate.current) {
            firstUpdate.current = false;
            return;
        }
        Router.push({ pathname: `/teams/${selectedFormat}` });
    }, [selectedFormat]);

    const handleChange = (event: SelectChangeEvent) => {
        setSelectedFormat(event.target.value as string);
    };

    return (
        <div>
            <FormControl size="small">
                <label className="font-light text-sm mb-1 text-zinc-700">
                    Select your format
                </label>
                <Select
                    labelId="ps-teams-format-dropdown-label"
                    value={
                        selectedFormat.toString() ??
                        Format.gen9vgc2023regulationd.toString()
                    }
                    onChange={handleChange}
                    className="min-w-[300px] sm:min-w-[560px] md:min-w-[570px] xl:min-w-[340px] text-zinc-700"
                >
                    {Object.keys(Format)
                        .filter((key) => isNaN(Number(key)))
                        .map((availableFormat, index) => (
                            <MenuItem
                                value={availableFormat.toString()}
                                key={index}
                                className="text-zinc-700"
                            >
                                <strong>{availableFormat.toString()}</strong>
                            </MenuItem>
                        ))}
                </Select>
            </FormControl>
        </div>
    );
};

export default PsTeamsFormatDropdown;
