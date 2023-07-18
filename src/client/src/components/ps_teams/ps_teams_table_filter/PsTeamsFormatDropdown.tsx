import { useRouter } from "next/router";
import { useState, useEffect } from "react";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import { Format } from "../../../../types";

const PsTeamsFormatDropdown = () => {
    // const [format, setFormat] = useState(
    //     Format.gen9vgc2023regulationd.toString()
    // );
    const [format, setFormat] = useState();

    const router = useRouter();

    // https://github.com/vercel/next.js/issues/18127#issuecomment-950907739
    // useEffect(() => {
    //     router.push(`/teams/${format}`);
    // }, [format]);

    const handleChange = (event: SelectChangeEvent) => {
        setFormat(event.target.value as string);
    };

    return (
        <div>
            <FormControl size="small">
                <label className="font-light text-sm mb-1 text-zinc-700">
                    Select your format
                </label>
                <Select
                    labelId="ps-teams-format-dropdown-label"
                    value={format}
                    onChange={handleChange}
                    className="min-w-[300px] sm:min-w-[560px] md:min-w-[570px] xl:min-w-[340px] text-zinc-700"
                >
                    {Object.keys(Format)
                        .filter((key) => isNaN(Number(key)))
                        .map((format, index) => (
                            <MenuItem
                                value={format.toString()}
                                key={index}
                                className="text-zinc-700"
                            >
                                <strong>{format.toString()}</strong>
                            </MenuItem>
                        ))}
                </Select>
            </FormControl>
        </div>
    );
};

export default PsTeamsFormatDropdown;
