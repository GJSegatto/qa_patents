"use client"

import * as React from 'react'
import { CheckIcon, ChevronsUpDownIcon } from "lucide-react"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList
 } from '@/components/ui/command'
 import {
    Popover,
    PopoverContent,
    PopoverTrigger
 } from "@/components/ui/popover"

 const llm_models = [
    {
        value: "gpt-5-nano",
        label: "GPT 5 Nano"
    },
    {
        value: "gpt-4.1-nano",
        label: "GPT 4.1 Nano"
    },
    {
        value: "gemini-2.5-flash",
        label: "Gemini 2.5 Flash"
    },
    {
        value: "gemini-2.5-pro",
        label: "Gemini 2.5 Pro"
    }
 ]

 interface LLMModelsListProps {
    onModelSelect: (model: string) => void;
    selectedModel: string;
 }

 export function LLMModelsList({ onModelSelect, selectedModel }: LLMModelsListProps) {
    const [open, setOpen] = React.useState(false)
    const [value, setValue] = React.useState("gpt-5-nano")

    return (
        <Popover open={open} onOpenChange={setOpen}>
            <PopoverTrigger asChild>
                <Button
                variant="outline"
                role="combobox"
                aria-expanded={open}
                className="w-auto justify-between"
                >
                {llm_models.find((model) => model.value === value)?.label}
                <ChevronsUpDownIcon className="ml-2 h-4 w-2 shrink-0 opacity-50" />
                </Button>
            </PopoverTrigger>
            <PopoverContent className="w-[200px] p-0">
                <Command>
                <CommandInput placeholder="Pesquise LLMs..." />
                <CommandList>
                    <CommandEmpty>Modelo não encontrado.</CommandEmpty>
                    <CommandGroup>
                    {llm_models.map((llm_model) => (
                        <CommandItem
                        key={llm_model.value}
                        value={llm_model.value}
                        onSelect={(currentValue) => {
                            setValue(currentValue);
                            onModelSelect(currentValue);
                            setOpen(false);
                        }}
                        >
                        <CheckIcon
                            className={cn(
                            "mr-2 h-4 w-4",
                            value === llm_model.value ? "opacity-100" : "opacity-0"
                            )}
                        />
                        {llm_model.label}
                        </CommandItem>
                    ))}
                    </CommandGroup>
                </CommandList>
                </Command>
            </PopoverContent>
    </Popover>
    )
    
 }